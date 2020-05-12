from flask import Flask, request, redirect
import math, random

app = Flask(__name__)
app.env = 'development'
app.debug = True

def check_positive_number(num):
    if not num.isnumeric():
        return -1
    elif int(num) <= 0:
        return -1
    else:
        return int(num)

def solve_save(filename, content):
    with open(f'./solve/{filename}', 'a', encoding='utf8') as f:
        f.write(content)
        f.write('\n\n')

@app.route('/')
def index():
    return "Welcome, Pair Program by 서치원,김수연"

# 사용자로부터 2 ~ 9 사이의 숫자를 입력 받은 후, 해당 숫자에 대한 구구단을 출력하세요.
# /gugu/<number>
@app.route('/gugu/<number>')
def tree(number):
    number = check_positive_number(number)
    
    if not(number >= 2 and number <= 9):
        return "invalid parameter"
    
    i = 1
    gugu_list = []
    gugu_list.append(f"{number} 단")
    while i<10:
        gugu_str = f'{i} * {number} = ' + str(i * number)
        i += 1
        gugu_list.append(gugu_str)
        
    solve_save(f'gugu.txt', '\n'.join(gugu_list))
    return '<br>'.join(gugu_list)

# 사용자로부터 숫자를 N을 입력받은 후 1부터 N까지의 숫자 중 소수만 출력하세요.
# /prime?num=N
@app.route('/prime')
def prime():
    
    num = request.args.get("num")
    num = check_positive_number(num)
    
    if num <= 0:
        return "invalid parameter"
    
    prime_list = [f"{num} 까지의 소수 목록", str(1)]
    
    for i in range(2, num + 1):

        is_prime = True
        
        sqrt = math.floor(math.sqrt(i))
        
        for j in range(2, sqrt + 1):
            if i%j == 0:
                is_prime = False
                break
            
        if is_prime:
            prime_list.append(str(i))
                  
    solve_save(f'prime.txt', '\n'.join(prime_list))
    return '<br>'.join(prime_list)

# 사용자로부터 숫자를 N을 입력받아. N의 약수를 모두 출력하세요.
# /common_factor?num=N

def factor(num):
    
    f_list = ['1']
    
    for i in range(2, num):
        if num % i == 0:
            f_list.append(str(i))
    f_list.append(str(num))

    return f_list

@app.route('/common_factor')
def common_factor():
    
    num = request.args.get("num")
    num = check_positive_number(num)
    
    if num <= 0:
        return "invalid parameter"
    
    factor_list = [f"{num} 의 약수 목록"]
    factor_list += factor(num)
                  
    solve_save(f'factor.txt', '\n'.join(factor_list))
    return '<br>'.join(factor_list)

# 사용자로부터 숫자를 N, M을 입력받아 N과 M의 최대공약수와 최소공배수를 출력하세요
# /commons?num1=N&num2=M
# 최대공약수: N,M 중에서 작은 수를 기준. 만약 min(N,M) = N 이라면 N의 약수 리스트를 내림차순 정렬. N의 가장 큰 약수부터 for문으로 반복하며 M의 약수 리스트 속에 있는지 여부 판단
# 최소공배수: N,M 중에서 큰 수를 기준. 만약 max(N,M) = M 이라면 for문으로 M을 배수로 증가시키면서 N으로 약분되는 지 체크 
@app.route('/commons')
def commons():
    num1 = request.args.get("num1")
    num2 = request.args.get("num2")
    num1 = check_positive_number(num1)
    num2 = check_positive_number(num2)
    
    if num1 <= 0 or num2 <= 0:
        return "invalid parameter" 

    # 최대공약수 계산 구역
    result_list = [f"{num1} {num2}의 최대공약수"]

    f1_list = factor(num1)
    f2_list = factor(num2)
    
    s1 = set(f1_list)
    s2 = set(f2_list)

    s = s1 & s2
    s = map(int, s)
    
    result_list.append(str(max(s)))
    
    # 최소공배수 계산 구역
    result_list.append(f"{num1} {num2}의 최소공배수")
    
    bigger = max([num1, num2])
    smaller = min([num1, num2])
    
    i = 1
    while True:
        if (bigger * i)%smaller == 0:
            break
        else:
            i += 1
        
    result_list.append(str(bigger * i))

    solve_save(f'commons.txt', '\n'.join(result_list))
    return '<br>'.join(result_list)

    # solve_save(f'comm.txt', '\n'.join(factor_list))

# 사용자로부터 숫자를 N을 입력받아, 1, 5, 10, 25, 50의 숫자를 이용하여 최소 갯수로 N을 표현해보자 
# 예) 183 = 50 * 3 + 25 * 1 + 5 * 1 + 1 * 3 => 총 8개
# /coins?num=N
# 가장 큰 수부터 먼저 N을 나누고 나머지를 그 다음 큰 수로 나누고... 
@app.route('/coins')
def coins():
    
    num = request.args.get("num")
    num = check_positive_number(num)
    
    if num <= 0:
        return "invalid parameter"

    coin_list = [50, 25, 10, 5, 1]
    div_list = []
    result_list = [f"{num}의 동전 나누기 결과"]
    
    mod = num
    
    for coin in coin_list:
        div_list.append(mod // coin)  
        mod = mod % coin
        
    result_str = f"{num} = "
    
    for i in range(len(coin_list)):
        if div_list[i] != 0:
            result_str += f"{coin_list[i]} * {div_list[i]} + "
    
    # 문자열 마지막 + 삭제
    result_str = result_str[:-2]
    
    result_list.append(result_str)

    solve_save(f'coins.txt', '\n'.join(result_list))
    return '<br>'.join(result_list)

# 주민등록번호를 입력받아 올바른 주민번호인지 검증하라.
# 주민번호 : ① ② ③ ④ ⑤ ⑥ - ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬
# 합계 
# = 마지막수를 제외한 12자리의 숫자에 2,3,4,5,6,7,8,9,2,3,4,5 를 순서대로 곱한수의 합
# = ①×2 + ②×3 + ③×4 + ④×5 + ⑤×6 + ⑥×7 + ⑦×8 + ⑧×9 + ⑨×2 + ⑩×3 + ⑪×4 + ⑫×5
# 나머지 = 합계를 11로 나눈 나머지
# 검증코드 = 11 - 나머지
# 여기서 검증코드가 ⑬자리에 들어 갑니다.
#
# /jumin 
# with form post

def verify_jumin(serial):
    
    mul_list = [2,3,4,5,6,7,8,9,2,3,4,5]
    s_list = list(serial)
    s_list.pop(6)
    origin_13th = int(s_list.pop())
    s_list = list(map(int, s_list))
    
    check = 0
    for i in range(len(s_list)):      
        check += s_list[i] * mul_list[i]
        
    print(f"check = {check}")
    print(f"13th = {origin_13th}")
    check_value = check % 11
    
    print(f"check_value = {check_value}")
    
    if check_value == 1:
        check_value = 0
    else: check_value = 11 - check_value   
    
    return (check_value == origin_13th) 

@app.route('/jumin_result')
def jumin_result():
    result = request.args.get('result')
    
    if result == "True":
        result_str = "입력하신 값은 유효합니다."
    else:
        result_str = "입력하신 값은 유효하지 않습니다."

    html = result_str
    html += "<br><br><input type='button' value='다시 입력' onClick='history.go(-1)'/>"
    
    return html

    
@app.route('/jumin', methods=['get', 'post'])
def jumin():
    if request.method == 'POST':
        serial = request.form.get('jumin')
        
        if len(serial) == 14 and serial[6] == '-':
            serial_num_check = serial.replace("-", "")
            
            if serial_num_check.isnumeric():
                result = verify_jumin(serial)
                    
                return redirect(f'/jumin_result?result={result}')
            else:
                return "invalid parameter"
        else:
            return "invalid parameter"
    else:
        with open('./jumin_check.html', 'r', encoding='utf8') as f:
            template = f.read()
    
        return template
    
@app.route('/pi', methods=['get', 'post'])
def pi():
    
    with open('./pi_check.html', 'r', encoding='utf8') as f:
        template = f.read()
    result = ""
    
    if request.method == 'POST':
        num = request.form.get("pi_iteration")
        iter_num = check_positive_number(num)
    
        if iter_num <= 0:
            return "invalid parameter"
        
        comp_cnt = 0
        for i in range(iter_num):
            x = random.random()
            y = random.random()
            distance = math.sqrt(x**2 + y**2)
            if distance <= 1: comp_cnt+=1
        
        result =  "PI is {0}".format(4 * (comp_cnt / iter_num))

    return template.format(result=result)

app.run()






