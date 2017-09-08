"""
首先谈到这个语言的定义和运行原理
该语言定义在这样一个环境之上：
你有一列无限长的小火车，每个车厢里装了一个数字，初始为0。
还有一个列车员，初始在最头上那节车厢上。
好了，你把你写的BrainFK程序交给列车员，列车员会做如下的事情：
从左向右、由上自下一个字符一个字符地读取你的程序
当读到`+`的时候，将所在车厢里的数字加一
当读到`-`的时候，将所在的车厢里的数字减一
当读到`>`的时候，跑到后一个车厢去
当读到`<`的时候，跑到前一个车厢去
当读到`[`的时候，如果该车厢里面的数字为0，则跳去执行下一个`]`之后的程序内容
当读到`]`的时候，如果该车想里面的数字不为0，则跳去执行上一个`[`之后的程序内容
当读到`.`的时候，将所在车厢里面的数字翻译成ASCII字符，显示在你的屏幕上
当读到`,`的时候，从等待使用者输入一个ASCII字符，转码成数字写进所在车厢里
"""


class Tape(object):
    """
    纸带
    """
    def __init__(self):
        self.tape = [0]
        self.position = 0

    def get(self):
        return self.tape[self.position]

    def set(self, val):
        self.tape[self.position] = val

    def inc(self):
        self.tape[self.position] += 1

    def dec(self):
        self.tape[self.position] -= 1

    def forward(self):
        self.position += 1
        if len(self.tape) <= self.position:
            self.tape.append(0)

    def backward(self):
        self.position -= 1


class BrainFuck(object):
    def __init__(self,program,tape_obj):
        self.program = program # program that you're going to interpret
        self.pairs = {}
        self.record()
        self.tape = tape_obj

    def record(self):
        """遍历一次代码，记录'['和']'的相对位置"""
        left_stack = []
        for i,p in enumerate(self.program):
            if p == '[':
                left_stack.append(i)
            if p == ']':
                left = left_stack.pop()
                right = i
                self.pairs[left] = right
                self.pairs[right] = left

    def parse(self):
        values = []
        pc = 0
        while pc < len(self.program):
            p = self.program[pc]
            if p == '+':
                self.tape.inc()
            elif p == '-':
                self.tape.dec()
            elif p == '>':
                self.tape.forward()
            elif p == '<':
                self.tape.backward()
            elif p == '[':
                if self.tape.get() == 0:
                    pc = self.pairs[pc]  # 到下一个]所在的地方
            elif p == ']':
                if self.tape.get() != 0:
                    pc = self.pairs[pc]
            elif p == '.':
                values.append(chr(self.tape.get()))
            elif p == ',':
                self.tape.set(input())
            pc += 1
        return ''.join(values)


if __name__ == '__main__':
    p = """++++++++++[>+++++++>++++++++++>+++>+<<<<-]
>++.>+.+++++++..+++.>++.<<+++++++++++++++.
>.+++.------.--------.>+.>."""
    p2 = '[-]>[-]>[-]++++[<+++++>-]<+++[<+++++>-]<. >++[<----->-]<-. ---.'
    tobj = Tape()
    obj = BrainFuck(p,tobj)
    print(obj.parse())