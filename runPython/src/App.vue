<template>
  <div class="main_container">
    <div class="codingEditor_container">
      <CodingEditor />
    </div>
    <div class="terminal_contianer">
      <CommandTerminal ref="terminal" />
    </div>
  </div>
</template>

<style scoped>
.main_container {
  /* display: flex; */
  width: 100%;
  height: 100vh;
}
.codingEditor_container {
  width: 100%;
  height: 70%;
}

.terminal_contianer {
  width: 100vw;
  height: 25%;
  /* height: 100%; */
}
</style>

<script setup>
import CodingEditor from '@/components/CodingEditor.vue'
import { ref } from 'vue'
import CommandTerminal from '@/components/CommandTerminal/CommandTerminal.vue'
// import { TerminalApi } from 'vue-web-terminal'

const terminal = ref()

// const code = ref(`import time
// print(1)
// time.sleep(3)
// print(2)`)

// // 处理编辑器内容变化的方法

// const stopRun = () => {
//   TerminalApi.execute('my-terminal', 'kill')
// }

// const runCode = async () => {
//   await saveCode()
//   terminal.value.TerminalApi.execute('my-terminal', 'python -u code_test.py')
//   return
// }

// const terminal = ref()
</script>
