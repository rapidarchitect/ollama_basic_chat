import sys
import hyperdiv as hd
import requests
from ollama import Client


"""
    Set the location for where ollama is running, default is based on default install
"""
ollama_url = 'http://localhost:11434'

# create an empty list to store all the models we have installed.
model_list = []

if requests.get(ollama_url).status_code == 200:
    client = Client(host=ollama_url)
    api_return = client.list()
    for model in api_return['models']:
        model_list.append(model['name'])
else:
    print("Ollama is not running")
    sys.exit(1)


def add_message(role, content, state, gpt_model):
    """
    Add a message to the state.

    Args:
        role (str): The role of the message (e.g., 'user', 'assistant').
        content (str): The content of the message.
        state (hd.state): The state object.
        gpt_model (str): The GPT model used for generating the message.
    """
    state.messages += (
        dict(role=role, content=content, id=state.message_id, gpt_model=gpt_model),
    )
    state.message_id += 1


def request(gpt_model, state):
    """
    Send a request to the Ollama chatbot API.

    Args:
        gpt_model (str): The GPT model to use for the request.
        state (hd.state): The state object.
    """
    response = client.chat(
        model=gpt_model,
        messages=[dict(role=m["role"], content=m["content"]) for m in state.messages],
        stream=True,
    )

    for chunk in response:
        message = chunk['message']
        state.current_reply += message.get("content", "")

    add_message("assistant", state.current_reply, state, gpt_model)
    state.current_reply = ""


def render_user_message(content, gpt_model):
    """
    Render a user message.

    Args:
        content (str): The content of the message.
        gpt_model (str): The GPT model used for generating the message.
    """
    with hd.hbox(
        align="center",
        padding=0.5,
        border_radius="medium",
        background_color="neutral-50",
        font_color="neutral-600",
        justify="space-between",
    ):
        with hd.hbox(gap=0.5, align="center"):
            hd.icon("chevron-right", shrink=0)
            hd.text(content)
        hd.badge(gpt_model)


def main():
    """
    Main function to run the Ollama Chatbot.
    """
    state = hd.state(messages=(), current_reply="", gpt_model="gpt-4", message_id=0)

    task = hd.task()

    template = hd.template(title="Ollama Basic Chatbot", sidebar=False)

    with template.body:
        if len(state.messages) > 0:
            with hd.box(direction="vertical-reverse", gap=1.5, vertical_scroll=True):
                if state.current_reply:
                    hd.markdown(state.current_reply)

                for e in reversed(state.messages):
                    with hd.scope(e["id"]):
                        if e["role"] == "system":
                            continue
                        if e["role"] == "user":
                            render_user_message(e["content"], e["gpt_model"])
                        else:
                            hd.markdown(e["content"])

        with hd.box(align="center", gap=1.5):
            with hd.form(direction="horizontal", width="100%") as form:
                with hd.box(grow=1):
                    prompt = form.text_input(
                        placeholder="Talk to Ollama",
                        autofocus=True,
                        disabled=task.running,
                        name="prompt",
                    )

                model = form.select(
                    options=model_list,
                    value="tinyllama",
                    name="gpt-model",
                    placeholder='tinyllama:latest'
                )

            if form.submitted:
                add_message("user", prompt.value, state, model.value)
                prompt.reset()
                task.rerun(request, model.value, state)

            if len(state.messages) > 0:
                if hd.button(
                    "Start Over", size="small", variant="text", disabled=task.running
                ).clicked:
                    state.messages = ()


hd.run(main)
