from hp_shared.base import BaseEnv
import subprocess
import asyncio


commandMap = {
  'windows': {
    'copy': 'clip',
    'paste': 'powershell get-clipboard',
  },
  'mac': {
    'copy': 'pbcopy',
    'paste': 'pbpaste',
  },
  'linux': {
    'copy': 'xclip -selection clipboard',
    'paste': 'xclip -selection clipboard -o',
  },
}

class clipboard:
  @classmethod
  async def writeText(cls, text):
    text = str(text)
    command = commandMap[BaseEnv.os]['copy']
    process = await asyncio.create_subprocess_shell(command, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process.communicate(input=text.encode('utf-8'))
    return text

  @classmethod
  async def readText(cls):
    command = commandMap[BaseEnv.os]['paste']
    process = await asyncio.create_subprocess_shell(command, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, *_ = await process.communicate()
    stdout = stdout.decode('utf-8').strip()
    return stdout

  @classmethod
  def writeTextSync(cls, text):
    text = str(text)
    command = commandMap[BaseEnv.os]['copy']
    subprocess.run(command, input=text.encode('utf-8'), check=True, shell=True)
    return text

  @classmethod
  def readTextSync(cls):
    command = commandMap[BaseEnv.os]['paste']
    stdout = subprocess.run(command, capture_output=True, check=True, shell=True, text=True, encoding='utf-8').stdout
    stdout = stdout.strip()
    return stdout

  # 简写方式
  @classmethod
  async def copy(cls, *args):
    return await cls.writeText(*args)

  @classmethod
  async def paste(cls, *args):
    return await cls.readText(*args)

  @classmethod
  def copySync(cls, *args):
    return cls.writeTextSync(*args)

  @classmethod
  def pasteSync(cls, *args):
    return cls.readTextSync(*args)

__all__ = ["clipboard"]
