import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    from langserve import RemoteRunnable

    full_chain = RemoteRunnable("http://localhost:8000/artefact_identification/")
    cl.user_session.set("chain", full_chain)

@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")  
    res = await chain.ainvoke({"question": message.content})
    
    # Display the answer directly
    await cl.Message(content=res).send()
