const express = require("express");
const app = express();
const port = process.env.PORT || 3000;
const { exec } = require("child_process");

app.get("/", (req, res) => {
  // 执行 pwd 命令
  exec("pwd", (err, stdout, stderr) => {
    if (err) {
      res.send("命令行执行出错：" + err);
    } else {
      res.send("当前工作目录为：\n" + stdout);
    }
  });
});

// 启动服务器
app.listen(port, () => console.log(`App is running on port ${port}`));
