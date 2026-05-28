import win32com.client
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()
skt_pl1 = part.CreateSketchPlane("スケッチ1","","PL,X","0",True,False,False,"","","",False,False)
part.BlankElement(skt_pl1,True)
skt_arc1 = part.CreateSketchCircle(skt_pl1,"","デフォルト","-37.134052392003085,24.499229586425272","114.42065669526625",True,True,False)
solid1 = part.CreateSolid("ソリッド1","","SS400")
part.SetElementColor(solid1,"225","225","225","0")
extrudeParam1 = part.CreateLinearSweepParam()
extrudeParam1.Name="押し出し1"
extrudeParam1.AddProfile(skt_pl1)
extrudeParam1.DirectionType="N"
extrudeParam1.DirectionParameter1="47.000000000000014"
extrudeParam1.RefByGeometricMethod=True
extrude1 = part.CreateLinearSweep(solid1,"+",extrudeParam1,False)



##############  ###############
p0pt=doc.CreateSTLOption()
FilePath=r"C:\Users\sasap\OneDrive\デスクトップ\今治\pro_merge\chatbot_project\scripttest_gn_1.stl"
doc.ExporAsSTL(  FilePath,   p0pt)
##############

doc.FitAllViews()

View=doc.GetViews()



View.SetDirection("+X","+Y",True )
FileName="test_bm_1.jpg"
View.ExportToBitmap(
FileName, 
"1024 ") 

View.SetDirection("+Z","+Y",True )
FileName="test_bm_2.jpg"
View.ExportToBitmap(
FileName, 
"1024 ") 


View.SetDirection("+Y","-X",True )
FileName="test_bm_3.jpg"
View.ExportToBitmap(
FileName, 
"1024" ) 

doc.close()
