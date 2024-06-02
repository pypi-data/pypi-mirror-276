# start min function

def big(n1,n2):
        if n1 > n2:
                x = str(n1)+' is bigger than '+str(n2)+'.'
                return x
        if n2 > n1:
                x = str(n2)+' is bigger than '+str(n1)+'.'
                return x
        if n1 == n2:
                x = 'These are equal!'
                return x
# end min function

# start max function

def small(n1,n2):

        if n1 < n2:
                result =  str(n1)+' is smaller than '+str(n2)+'.'
                return result
        if n2 < n1:
                x = str(n2)+' is smaller than '+str(n1)+'.'
                return x
        if n1 == n2:
                x = 'These are equal!'
                return x

# end max function

# start add function

def add(n1,n2):
	x = n1 + n2
	z = str(n1) + ' + '+ str(n2) + ' = ' + str(x)
	return z

# end add function

# start sub function

def sub(n1,n2):
	x = n1 - n2
	z = str(n1) + ' - '+ str(n2) + ' = ' + str(x)
	return z

# end sub function

# start mul function

def mul(n1,n2):
	x = n1 * n2
	z = str(n1) + ' * '+ str(n2) + ' = ' + str(x)
	return z

# end mul function

# start div function

def div(n1,n2):
	if n2 != 0:
		x = n1 / n2
		z = str(n1) + ' / '+ str(n2) + ' = ' + str(x)
		return z

# end div function
