<p align="center">
  <picture>    
    <img alt="auto-coder" src="./logo/auto-coder.jpeg" width=55%>
  </picture>
</p>

<h3 align="center">
Auto-Coder (powered by Byzer-LLM)
</h3>

<p align="center">
| <a href="./docs/en"><b>English</b></a> | <a href="./docs/zh"><b>中文</b></a> |

</p>

---

*Latest News* 🔥

- [2024/05] Release Auto-Coder 0.1.68
- [2024/04] Release Auto-Coder 0.1.46
- [2024/03] Release Auto-Coder 0.1.25
- [2024/03] Release Auto-Coder 0.1.24

---

Auto-Coder is a command-line tool with YAML-based configuration that can automatically develop your existing project based on your requirements. 


## Installation

```shell
conda create --name autocoder python=3.10.11
conda activate autocoder
pip install -U auto-coder
## if you want to use private/open-source models, uncomment this line.
# pip install -U vllm
ray start --head
```

## Tutorial

1. [Setup auto-coder](./docs/en/000-AutoCoder_Preparation_Journey)
2. [AutoCoder_准备旅程](./docs/zh/000-AutoCoder_准备旅程.md)

## Example Project

https://github.com/allwefantasy/auto-coder.example
