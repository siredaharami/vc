import asyncio
import io
import os
import sys
import traceback

from pyrogram import filters, Client
from pyrogram.types import Message

from BADUC import mongodb as database
from BADUC.database.gchat import ReplyCheck

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

@app.on_message(bad(["eval"]) & (filters.me | filters.user(SUDOERS)))
async def eval_func_init(app, message):
    await evaluation_func(app, message)




async def evaluation_func(app: Client, message: Message):
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        reply = message.reply_to_message or None
        await aexec(cmd, app, message, reply, database)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "<b>Expression</b>:\n<code>{}</code>\n\n<b>Result</b>:\n<code>{}</code> \n".format(
        cmd, evaluation.strip()
    )

    if len(final_output) > 4096:
        with open("eval.txt", "w", encoding="utf8") as out_file:
            out_file.write(str(final_output))

        await message.reply_document(
            "eval.txt",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=ReplyCheck(message),
        )
        os.remove("eval.txt")
        await status_message.delete()
    else:
        await status_message.edit(final_output)


async def aexec(code, b, m, r, d):
    sys.tracebacklimit = 0
    exec(
        "async def __aexec(b, m, r, d): "
        + "".join(f"\n {line}" for line in code.split("\n"))
    )
    return await locals()["__aexec"](b, m, r, d)


@app.on_message(bad(["exec"]) & (filters.me | filters.user(SUDOERS)))
async def execution_func_edited(app, message):
    await execution(app, message)



@app.on_message(bad(["exec"]) & (filters.me | filters.user(SUDOERS)))
async def execution_func(app, message):
    await execution(app, message)


async def execution(app: Client, message: Message):
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No errors"
    o = stdout.decode()
    if not o:
        o = "No output"

    OUTPUT = ""
    OUTPUT += f"<b>Command:</b>\n<code>{cmd}</code>\n\n"
    OUTPUT += f"<b>Output</b>: \n<code>{o}</code>\n"
    OUTPUT += f"<b>Errors</b>: \n<code>{e}</code>"

    if len(OUTPUT) > 4096:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await message.reply_document(
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=ReplyCheck(message),
        )
        os.remove("exec.text")
    else:
        await message.reply_text(OUTPUT)
