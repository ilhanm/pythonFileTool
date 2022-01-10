from FileTool import FileTool
myft=FileTool("products.csv",["name","price","quantity"])


#myft.addRow({"name":"Playstation 5","price":855,"quantity":12})
#myft.addRow(["mikrofon",12,23])
#myft.deleteRow(5)
#myft.getAll()
#myft.mergeAnotherFile("yeniUrunler.csv")

myft.Menu()
