<p align="center">
<img alt = "Hash Logo"
    src="https://imgs.search.brave.com/iAAnnRR2ONM-VoncrfU0CPNANZa0k_KNWyt3oULrKw4/rs:fit:500:0:0/g:ce/aHR0cHM6Ly93d3cu/bG9naW5yYWRpdXMu/Y29tL2Jsb2cvc3Rh/dGljLzlmNjBkOGEx/MmUyY2I5MjQwYmZl/NTRiNTQ1MTViNDJh/LzA0ZmY2L2VuY3J5/cHRpb24tYW5kLWhh/c2hpbmcucG5n">
</p>


## Contents

- [Introduction](#introduction)
- [Usage](#usage)
- [Test](#Test)
- [Description](#description)

## Introduction
The hash algorithm is a one-way digest algorithm that can be utilized in various applications leveraging its features. The code provided implements a distinct hash algorithm that can be used to hash hexadecimal strings of less than 64 characters.

## Usage
```bash
python main.py
```

## Test
```bash
python tests/test.py
```

## Description
The implemented hash algorithm is composed of several layers of abstraction:

At the first level of abstraction, 2<sup>work_factor</sup> number of Box components are executed, and in each step, the XOR of the salt and the output of the previous step is the input to the next step.


At the second level of abstraction, each <b>Box</b> component is composed of other components called Round and LastRound, where the Round component is executed 32 times, and in each step, the output of the previous step is the input to the next step. Finally, the output of the 32nd Round is the input to the LastRound.
