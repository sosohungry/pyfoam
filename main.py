from changfile import *
from setDefault import setDefault

def main():

    # 加载修改文件
    source_path = "./example"


    print("-------------------------------------------------")
    print("-                                               -")
    print("-                                               -")
    print("-               changefilesystem                -")
    print("-                                               -")
    print("-                                               -")
    print("-                                               -")
    print("-------------------------------------------------")
    print("Chose the file you want to change!")
    print("number 1, change viscosity")
    print("number 2, change tension")
    print("number 3, change speed")
    print("number 4, change lubricity")
    # print("number 5, change flow_line")
    # print("numbe 6, change extract")
    print("input q to exit!")

    flag = 1


    while (flag==1):

        inputNum = input("please input number you want:")

        if(inputNum=='q'):
            flag = 0
            continue
    
        else:
            number = int(inputNum)

        print("the number you choose is:", number)

        if number==1:
            input_water = input("please input water:")
            input_oil = input("please input oil:")
            input_water_num = input_water.split(" ")
            input_oil_num = input_oil.split(" ")
            print(input_water_num)
            print(type(input_water_num))
            print("\n")
            print(input_oil_num)
            for i in range(len(input_oil_num)):
                changeViscosity(source_path, input_water_num[i], input_oil_num[i], True)


        elif number==2:
            input_num = input("please input tension number:")
            input_num_split = input_num.split(" ")
            for i in range(len(input_num_split)):
                changeTension(source_path, input_num_split[i], True)

        elif number==3:
            boundaryName = input("please input boundaryName:")
            input_num = input(r"please input number(every example please use \t to split):")
            print(boundaryName)
            print(input_num)
            input_num_split = input_num.split("\t")
            print(input_num_split)
            for i in range(len(input_num_split)):
                changeVelocity(source_path, boundaryName, input_num_split[i], True)

        elif number==4:
            boundaryName = input("please input boundaryName:")
            input_num = input(r"please input number:")
            print(boundaryName)
            print(input_num)
            input_num_split = input_num.split(" ")
            print(input_num_split)
            for i in range(len(input_num_split)):
                changeLubricity(source_path, boundaryName, input_num_split[i], True)
        elif number==5:
            print("please setDefault:")
            setDefault(source_path)
      
if __name__ == "__main__":

    # 程序入口
    source_path = "./example"
    main()
    
   
   
    



   
