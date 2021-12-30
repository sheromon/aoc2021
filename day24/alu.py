import numpy as np

class Alu:

    def __init__(self, steps, input_list, constants=None, gen_expressions=False):
        """Initialize ALU.

        :param steps: list of instructions, where each instruction is a list
            of two to three strings (two for inputs and three for operations)
        :param input_list: list of integers
        :param constants: optional sequence of values that can be used instead
            of computing a result for each step; length should be equal to the
            number of instructions; if None, all ALU states will be computed on
            the fly; defaults to None
        :param gen_expressions: optional boolean; if True, string expressions
            will be generated for each variable (e.g. "(inp 0 + 2) * 26")
        """
        self.steps = steps
        self.ins_ind = 0  # keep track of which instruction we're on
        if isinstance(input_list, str):
            input_list = [int(char) for char in input_list]
        self.input_list = input_list
        self.inp_ind = 0  # keep track of which input value we're on
        # will hold the current value for each variable
        self.vals = {name: 0 for name in ['w', 'x', 'y', 'z']}
        # store intermediate results after each instruction
        self.intermeds = []
        # constants with values not equal to -1 will be used for that step
        # pretty sure the states never go negative, so this should be okay to do
        if constants is None:
            constants = -1 * np.ones(len(self.steps))
        self.constants = constants
        self.gen_expressions = gen_expressions
        # will hold the string expressions for each variable
        self.exprs = {name: '0' for name in ['w', 'x', 'y', 'z']}

    def run(self, max_steps=None):
        """Run the ALU until the max number of steps has been reached.

        :param max_steps: optional integer specifying the maximum number of
            instructions to process; if None, will use the length of the
            instruction list; defaults to None
        """
        if max_steps is None:
            max_steps = len(self.steps)
        for _ in self.steps[:max_steps]:
            self.step()
        return self

    def step(self):
        """Run one step of the ALU processing."""
        instruction = self.steps[self.ins_ind]
        op = instruction[0]
        name = instruction[1]
        if op == 'inp':
            ind = self.inp_ind
            self.inp_ind += 1
            self.vals[name] = int(self.input_list[ind])
            self.exprs[name] = f'{op} {ind}'
        else:
            self.process_operation(instruction)
        self.intermeds.append(self.vals[name])
        self.ins_ind += 1

    def process_operation(self, instruction):
        """Perform one ALU operation."""
        op, name, expr2 = instruction
        # if we're using a constant for this step, we don't need to do any
        # calculations, and the string expresison is straightforward too
        if self.constants[self.ins_ind] != -1:
            self.vals[name] = self.constants[self.ins_ind]
            if self.gen_expressions:
                self.exprs[name] = str(self.constants[self.ins_ind])
            return
        # otherwise, we have to do some work
        name2 = None
        try:
            val = int(instruction[2])
        except:
            name2 = instruction[2]
            expr2 = self.exprs[name2]
            val = self.vals[name2]
        if op == 'add':
            op_str = '+'
            self.vals[name] += val
        elif op == 'mul':
            op_str = '*'
            self.vals[name] *= val
        elif op == 'div':
            op_str = '//'
            self.vals[name] = self.vals[name] // val
        elif op == 'mod':
            op_str = '%'
            self.vals[name] = self.vals[name] % val
        elif op == 'eql':
            op_str = '=='
            self.vals[name] = int(self.vals[name] == val)
        if self.constants[self.ins_ind] != -1:
            self.vals[name] = self.constants[self.ins_ind]

        if self.gen_expressions:
            # if we're multiplying by 0, just put a zero in there
            if op == 'mul' and val == 0:
                self.exprs[name] = '0'
            # some operations don't change the value (mul or div by 1 or add 0),
            # so don't update the expression if it's not changing
            elif not (val == 1 and op in ['mul', 'div']) or (val == 0 and op == 'add'):
                self.exprs[name] = f'{self.exprs[name]} {op_str} {expr2}'
            # simplify expressions if it's easy
            if self.exprs[name].startswith('0 + '):
                self.exprs[name] = self.exprs[name][4:]
            elif self.exprs[name].startswith('0 * '):
                self.exprs[name] = '0'
            # add parentheses for clarity?
            if len(self.exprs[name]) > 2 and op not in ['mul', 'div']:
                self.exprs[name] = '(' + self.exprs[name] + ')'
