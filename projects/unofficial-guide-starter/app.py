"""
app.py - Milestone 5b: Query Interface

A styled gradio chat UI. The user types a PC question (or clicks an example),
and we run the full pipeline (retrieve -> generate) and show a grounded answer
with its sources.

Run it:  python app.py   (then open the local URL it prints)

Prerequisite: build the vector store first with  python embed_store.py
"""

import gradio as gr

from generate import generate_answer

# These stay visible as buttons the whole time (they don't disappear after you ask).
EXAMPLES = [
    "My pc is running slow",
    "Nobody can hear me on zoom call.",
    "Chrome is taking a long time to load",
    "what should i name my folder",
    "How do I find a file",
]


# ---------------------------------------------------------------------------
# Chat handler
# ---------------------------------------------------------------------------

def respond(message, history):
    """
    Take the user's message + the running chat history, produce an answer,
    and return the updated history (plus an empty string to clear the textbox).

    `history` is a list of {"role": ..., "content": ...} dicts (gradio's
    "messages" format, which is the default in gradio 6).
    """
    if not message.strip():
        return history, ""

    answer, hits = generate_answer(message)
    sources = ", ".join(sorted({h["source"] for h in hits}))
    reply = f"{answer}\n\n---\nSources: {sources}"

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return history, ""


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

with gr.Blocks(title="The Unofficial Guide") as demo:

    gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#312e81; margin:0;">
                The Unofficial Guide
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Fix your PC, browser, and files - answers straight from the official guides.
            </p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                height=440,
                placeholder=(
                    "<div style='text-align:center; color:#9ca3af; margin-top:3rem;'>"
                    "Ask a PC question to get started"
                    "</div>"
                ),
            )
            msg = gr.Textbox(
                placeholder="e.g. My PC is running slow",
                container=False,
            )

            # These example buttons STAY on screen the whole time.
            gr.Markdown("**Try one of these:**")
            with gr.Row():
                example_buttons = [gr.Button(q, size="sm") for q in EXAMPLES]

        with gr.Column(scale=1, min_width=180):
            gr.HTML("""
                <div style="background:#f5f3ff; border:1px solid #ddd6fe;
                            border-radius:10px; padding:1rem; margin-top:0.5rem;">
                    <p style="font-size:0.8rem; font-weight:700; color:#4c1d95;
                               margin:0 0 0.5rem; letter-spacing:0.05em;">
                        LOADED GUIDES
                    </p>
                    <ul style="font-size:0.85rem; color:#5b21b6; list-style:none;
                                padding:0; margin:0; line-height:1.8;">
                        <li>PC Performance</li>
                        <li>Free Up Storage</li>
                        <li>Task Manager</li>
                        <li>Resource Monitor</li>
                        <li>Chrome Browser</li>
                        <li>Edge Browser</li>
                        <li>Video Conferencing</li>
                        <li>File Explorer</li>
                        <li>File Naming</li>
                        <li>Organize Folders</li>
                    </ul>
                    <hr style="border:none; border-top:1px solid #ddd6fe; margin:0.75rem 0;">
                    <p style="font-size:0.75rem; color:#7c3aed; margin:0; line-height:1.5;">
                        Answers are grounded in the loaded guides only. If something
                        isn't in them, the bot will say so.
                    </p>
                </div>
            """)

    # Submitting the textbox runs respond() and clears the box.
    msg.submit(respond, [msg, chatbot], [chatbot, msg])

    # Each example button sends its own question through the same handler.
    # (q=q captures this button's text so every button keeps its own question.)
    for btn, q in zip(example_buttons, EXAMPLES):
        btn.click(lambda history, q=q: respond(q, history), [chatbot], [chatbot, msg])


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  The Unofficial Guide - starting up")
    print("=" * 50 + "\n")
    # Gradio 6 moved `theme` from gr.Blocks(...) to launch().
    demo.launch(theme=gr.themes.Soft(primary_hue="indigo"))
