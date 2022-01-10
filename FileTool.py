import csv
import json

class FileTool:    
    id=0
    idList=[]    
    elemDict=[]
    
    def __init__(self,path,fields=[]):
        self.path=path
        if fields==[]:
            self.setHeaders()
        else:
            self.fields=fields
        self.csvToDict()

    def setHeaders(self):      
        self.file=open(self.path,"r+")
        csv_reader = list(csv.reader(self.file, delimiter=','))        
        self.fields=csv_reader[0]
        
    def csvToDict(self):
        """
        Transfer csv row elements to a python iterable object.
        """        
        elemlist=[]
        self.file=open(self.path,"r+",encoding="UTF-8")
        csv_reader = list(csv.reader(self.file, delimiter=','))        
        for row in csv_reader[1:]:
            elemlist.append(row)
            self.idList.append(self.id)
            self.id=self.id+1
        self.elemDict=dict(zip(self.idList,elemlist))
    
    def getAll(self):
        """
        Reads all rows of given file.
        """
        print(f"FIELDS: {self.fields}")
        for id, element in self.elemDict.items():
            print(f"ID: {id} | {element}")
  
    def getRange(self,start :int,end :int):
        """
        Reads part of the given file.
        start: first row to read\n
        end: last row to read\n
        """
        for id, element in list(self.elemDict.items())[start:end+1]:
            print(f"ID: {id} | {element}")

    def getByID(self,rowID):
        print(f"ID: {rowID} | {self.elemDict[rowID]}")

    def addRow(self, element):
        """
        Adds new row to file with dict or list type.\n
        Iterable argument, list or dict type accepted
        """        
        if(isinstance(element,dict)): #add new row by using dict data type            
            self.elemDict[self.id]=list(element.values())
            self.idList.append(self.id)
            self.id+=1
            
        if(isinstance(element,list)): #add new row by using list data type
            self.elemDict[self.id]=element
            self.idList.append(self.id)
            self.id+=1
        self.saveChanges()

    def addMultiple(self,elems):
        if(isinstance(elems,list)): #add new row by using list data type
            for newElement in elems:
                self.addRow(newElement)
            print("Items added successfully")
            self.saveChanges()

    def deleteRow(self,rowId=-1):
        """
        Delete Row, optionally by id
        To remove specific row, pass rowId as argument\n
        If row id is not specified, last row will be deleted.
        """
        if(rowId==-1): 
            self.elemDict.popitem()
            self.idList.pop()
        else: 
            del self.elemDict[rowId]
            self.idList.pop(rowId)
        self.saveChanges()
        print("Item deleted successfully")

    def updateByID(self,rowId: int, newElement):
        """
        Update data by RowId\n
        rowId is the item id that you want to change \n
        newElement is changed version of this row which is DICT or LIST type.        
        """       
        
        if(isinstance(newElement,dict)):
            self.elemDict[rowId]=list(newElement.values())
            self.saveChanges()
        if(isinstance(newElement,list)): 
            self.elemDict[rowId]=newElement
            self.saveChanges()
        print("Item updated successfully")

    def saveChanges(self): #writes final version of list to the csv file 
        f=open(self.path,'w', newline='\n',encoding="UTF-8")
        _writer=csv.writer(f)
        _writer.writerow(self.fields)
        _writer.writerows(list(self.elemDict.values()))

    def Menu(self):
        
        mainMenu="""
        FILE OPERATIONS MENU
        [1]Reading
        [2]Adding
        [3]Updating
        [4]Deleting
        [5]Save as JSON
        [6]Merge Another File
        [7]Quit
        """
        while(1):
            print(mainMenu)            
            choice= int(input("Choose an operation [1-7]: "))
            if choice==7: break
            elif 0<choice<7: self.MenuOperations(choice)
            else: print("unvalid choice, please enter value between 1-7\n")            
              
    def MenuOperations(self,choice):
        newElement=[] 
        if choice==1:
            self.getAll()
        if choice ==2:                   
            for field in self.fields:
                newElement.append(input(f"Enter a value to set '{field}' field: "))                         
            self.addRow(newElement)
        if choice ==3:
            rowID=int(input("ID That You Want To Change: "))            
            newElement=[]
            print(f"Item that you want to change is: {self.elemDict[rowID]}")
            for field in self.fields:
                newElement.append(input(f"Enter a value to set '{field}' field: "))
            self.updateByID(rowID,newElement)
            self.saveChanges()
        if choice ==4:
            rowID=int(input("ID That You Want To Delete: "))
            self.deleteRow(rowID)
        if choice ==5: #to JSON
            self.ConvertJSON()
        if choice ==6:
            newFilePath=input("Enter your full file path with '.csv' or '.json' : ")
            self.mergeAnotherFile(newFilePath)
    
    def ConvertJSON(self):
        productDetails={}
        jsonResult={}
        myid=0
        for pdInfo in self.elemDict.values():
            for i,field in enumerate(self.fields):                
                productDetails[f"{field}"]=pdInfo[i]
            jsonResult[f"{myid}"]=productDetails.copy()
            myid=myid+1

        #print(jsonResult)
        result=json.dumps(jsonResult,indent=4)
        with open("output.json", "w", encoding="utf8") as outfile:
            outfile.write(result)  
        print("Items saved to 'output.json' file.")
    def mergeAnotherFile(self,path :str):        
        
        if path.endswith('csv'):
            try:
                file=open(path,"r+",encoding="UTF-8")
                csv_reader = list(csv.reader(file, delimiter=','))
                self.addMultiple(csv_reader)
                print(f"{path} file successfully combined with {self.path}")
            except:
                print("file not found or content unmatched")
        elif path.endswith('json'):
            try:
                with open('newdata.json') as json_file:
                    data = json.load(json_file) 
                    newItemsList=[]
                    jsvals=list(data)
                    for elem in jsvals:
                        newItemsList.append(list(elem.values()))
                    self.addMultiple(newItemsList)
                    print(f"{path} file successfully combined with {self.path}")
            except:
                print("file not found or content unmatched")

        else:
            print("unvalid file type")