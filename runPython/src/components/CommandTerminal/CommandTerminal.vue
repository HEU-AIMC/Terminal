<template>
  <terminal
    name="my-terminal"
    @exec-cmd="onExecCmd"
    :drag-conf="dragConf"
    @on-keydown="onKeydown"
    v-bind="terminalProps"
  />
</template>
<script setup>
import { watch, ref, reactive } from 'vue'
import { TerminalApi } from 'vue-web-terminal'
import { useWebSocket } from '@vueuse/core'
const { status, data, send, open, close } = useWebSocket('ws://127.0.0.1:8000/ws/run_python/', {
  onMessage(ws, event) {
    console.log('push')
    messageList.push(event.data)
  }
})
const messageList = reactive([])
const isCommandRunning = ref(false)
const currentCommand = ref('')
const fileName = 'code_test.py'
const dragConf = {
  width: '50%',
  height: '70%',
  zIndex: 100,
  init: {
    x: 200,
    y: 200
  },
  pinned: false
}

const terminalProps = {
  // dragConf,
  context: fileName,
  contextSuffix: '> ',
  showHeader: false
}

defineExpose({
  isCommandRunning
})
const onExecCmd = (key, command, success, failed, name) => {
  if (command === 'kill') {
    messageList.length = 0
    success({ type: 'info', content: 'Command killed' })
    send(command)
    isCommandRunning.value = false
    return
  }
  if (isCommandRunning.value) {
    console.log('正在执行命令，请稍后再试')
    return
  }
  send(command)
  isCommandRunning.value = true
  currentCommand.value = command

  const timer = setInterval(() => {
    console.log(
      messageList.length,
      'lengthlengthlengthlengthlength',
      isCommandRunning.value,
      !messageList.length,
      !isCommandRunning.value && !messageList.length
    )
    if (!isCommandRunning.value && !messageList.length) {
      clearInterval(timer)
    }
    const val = messageList.shift()
    if (val === undefined) {
      return
    }
    console.log(val)
    if (val.startsWith('start_')) {
      console.log('后端开始执行命令', val)
      return
    }
    if (val.startsWith('end_')) {
      success('')
      isCommandRunning.value = false
      return
    }
    if (val === 'killed') {
    }
    TerminalApi.pushMessage(name, { type: 'normal', content: val })
  }, 10)
}
const onKeydown = (event) => {
  if (event.key === 'c' && event.ctrlKey) {
    console.log('aaaaaaaaaaaa')
    TerminalApi.execute('my-terminal', 'kill')
    event.preventDefault()
  }
}
</script>
<style scoped></style>
