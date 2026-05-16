#定義一個簡單的函式
def say_hello():
    print("Hello")

#定義一格可以[接收函式]當作參數的函式
def run_with_announce(func):
    print("開始執行函式")
    func() #呼叫傳入的函式
    print("結束執行函式")


print("直接呼叫函式")
say_hello() #直接呼叫函式

print()
print("透過run_with_announce呼叫")
run_with_announce(say_hello) #把say_hello當參數傳進去(不加括號)

print("---------------------")

#========================
#第二段:包裝函式(裝飾詞原理)
#========================
#核心概念:用函式包裝另一個函式,讓被包裝的函式在執行前後都會有一些額外的行為
#就像在禮物外面包包裝紙一樣
def gift_wrap(func):
    def wrapper():
        print("開始執行函式")
        func() #呼叫傳入的函式
        print("結束執行函式")
    return wrapper #回傳包裝好的函式

def say_hello():
    print("Hello")


#手動包裝:把say_hello傳進去，得到包裝後的新版本
say_hello = gift_wrap(say_hello) #得到包裝後的新版本

#現在的say_hello已經是包裝過的版本了
say_hello() #呼叫包裝過的版本