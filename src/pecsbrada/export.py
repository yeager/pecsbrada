"""Export/print functionality for PECS-bräda."""

import csv
import io
import json
from datetime import datetime

import gettext
_ = gettext.gettext

from pecsbrada import __version__

APP_LABEL = "PECS-bräda"
AUTHOR = "Daniel Nylander"

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib


def sentence_to_csv(words, categories):
    """Export current sentence and available cards as CSV."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([_("Current Sentence")])
    writer.writerow([" ".join(words) if words else _("(empty)")])
    writer.writerow([])
    writer.writerow([_("Category"), _("Card"), _("Emoji")])
    for cat_name, items in categories.items():
        for emoji, label, term in items:
            writer.writerow([cat_name, label, emoji])
    writer.writerow([])
    writer.writerow([f"{APP_LABEL} v{__version__} — {AUTHOR}"])
    return output.getvalue()


def sentence_to_json(words, categories):
    """Export as JSON."""
    data = {
        "app": APP_LABEL,
        "version": __version__,
        "author": AUTHOR,
        "exported": datetime.now().isoformat(),
        "current_sentence": words,
        "categories": {
            cat: [{"emoji": e, "label": l, "term": t} for e, l, t in items]
            for cat, items in categories.items()
        },
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def sentence_to_pdf(words, output_path):
    """Export current sentence as visual A4 PDF."""
    try:
        import cairo
    except ImportError:
        try:
            import cairocffi as cairo
        except ImportError:
            return False

    width, height = 595, 842
    surface = cairo.PDFSurface(output_path, width, height)
    ctx = cairo.Context(surface)

    # Title
    ctx.set_font_size(24)
    ctx.move_to(40, 50)
    ctx.show_text(_("My Sentence"))

    ctx.set_font_size(12)
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.move_to(40, 70)
    ctx.show_text(datetime.now().strftime("%Y-%m-%d %H:%M"))
    ctx.set_source_rgb(0, 0, 0)

    # Sentence in large text
    ctx.set_font_size(32)
    sentence = " ".join(words) if words else _("(empty)")
    ctx.move_to(40, 140)
    ctx.show_text(sentence)

    # Individual words as cards
    y = 200
    ctx.set_font_size(20)
    for word in words:
        if y > height - 60:
            surface.show_page()
            y = 40
        # Card box
        ctx.set_source_rgb(0.95, 0.95, 0.95)
        ctx.rectangle(40, y, width - 80, 50)
        ctx.fill()
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(60, y + 33)
        ctx.show_text(word)
        y += 60

    # Footer
    ctx.set_font_size(9)
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.move_to(40, height - 20)
    ctx.show_text(f"{APP_LABEL} v{__version__} — {AUTHOR} — {datetime.now().strftime('%Y-%m-%d')}")

    surface.finish()
    return True


def show_export_dialog(window, words, categories, status_callback=None):
    """Show export dialog."""
    dialog = Adw.AlertDialog.new(
        _("Export"),
        _("Choose export format:")
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("csv", _("CSV"))
    dialog.add_response("json", _("JSON"))
    dialog.add_response("pdf", _("PDF"))
    dialog.set_default_response("pdf")
    dialog.set_close_response("cancel")
    dialog.connect("response", _on_export_response, window, words, categories, status_callback)
    dialog.present(window)


def _on_export_response(dialog, response, window, words, categories, status_callback):
    if response == "cancel":
        return
    if response == "csv":
        content = sentence_to_csv(words, categories)
        _save_text(window, content, "csv", status_callback)
    elif response == "json":
        content = sentence_to_json(words, categories)
        _save_text(window, content, "json", status_callback)
    elif response == "pdf":
        _save_pdf(window, words, status_callback)


def _save_text(window, content, ext, status_callback):
    fd = Gtk.FileDialog.new()
    fd.set_title(_("Save Export"))
    fd.set_initial_name(f"pecsbrada_{datetime.now().strftime('%Y%m%d')}.{ext}")
    fd.save(window, None, _on_text_done, content, ext, status_callback)


def _on_text_done(fd, result, content, ext, status_callback):
    try:
        gfile = fd.save_finish(result)
    except GLib.Error:
        return
    try:
        with open(gfile.get_path(), "w") as f:
            f.write(content)
        if status_callback:
            status_callback(_("Exported %s") % ext.upper())
    except Exception as e:
        if status_callback:
            status_callback(_("Export error: %s") % str(e))


def _save_pdf(window, words, status_callback):
    fd = Gtk.FileDialog.new()
    fd.set_title(_("Save PDF"))
    fd.set_initial_name(f"pecsbrada_{datetime.now().strftime('%Y%m%d')}.pdf")
    fd.save(window, None, _on_pdf_done, words, status_callback)


def _on_pdf_done(fd, result, words, status_callback):
    try:
        gfile = fd.save_finish(result)
    except GLib.Error:
        return
    try:
        ok = sentence_to_pdf(words, gfile.get_path())
        if ok and status_callback:
            status_callback(_("PDF exported"))
        elif not ok and status_callback:
            status_callback(_("PDF export requires pycairo"))
    except Exception as e:
        if status_callback:
            status_callback(_("Export error: %s") % str(e))
