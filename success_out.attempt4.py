import win32com.client
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.ShowMainWindow(True)
doc = evoship.Create3DDocument()
part = doc.GetPart()
skt_pl1 = part.CreateSketchPlane("Sketch3","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl1,True)
skt_ln1 = part.CreateSketchLine(skt_pl1,"","デフォルト","2926.4779204678048,400","12241.442807836524,400",False)
skt_pl2 = part.CreateSketchPlane("HK.Az.Wall","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl2,True)
skt_ln2 = part.CreateSketchLine(skt_pl2,"","作図","0,-18500","0,18500",False)
skt_ln3 = part.CreateSketchLine(skt_pl2,"","作図","-50000,15500","250000,15500",False)
skt_ln4 = part.CreateSketchLine(skt_pl2,"","作図","-50000,-15500","250000,-15500",False)
skt_layer1 = part.CreateSketchLayer("Casing.Fore",skt_pl2)
skt_ln5 = part.CreateSketchLine(skt_pl2,"","Casing.Fore","11370.000000000002,-10394.984078409721","11370.000000000002,9605.0159215902786",False)
skt_layer2 = part.CreateSketchLayer("Casing.Aft",skt_pl2)
skt_ln6 = part.CreateSketchLine(skt_pl2,"","Casing.Aft","4019.9999999999995,-10394.984078409721","4019.9999999999995,9605.0159215902786",False)
skt_layer3 = part.CreateSketchLayer("Casing.Side.P",skt_pl2)
skt_ln7 = part.CreateSketchLine(skt_pl2,"","Casing.Side.P","-1500,4800","18500,4800",False)
skt_layer4 = part.CreateSketchLayer("Casing.Side.S",skt_pl2)
skt_ln8 = part.CreateSketchLine(skt_pl2,"","Casing.Side.S","-1500,-4800","18500,-4800",False)
skt_layer5 = part.CreateSketchLayer("Dim.CenterLine",skt_pl2)
skt_ln9 = part.CreateSketchLine(skt_pl2,"","Dim.CenterLine","-50000,0","250000,0",False)
extrudeParam1 = part.CreateLinearSweepParam()
extrudeParam1.AddProfile(skt_pl2+",Casing.Aft")
extrudeParam1.DirectionType="2"
extrudeParam1.DirectionParameter1="50000"
extrudeParam1.DirectionParameter2="10000"
extrudeParam1.SweepDirection="+Z"
extrudeParam1.Name="HK.Casing.Wall.Aft"
extrudeParam1.MaterialName="SS400"
extrudeParam1.IntervalSweep=False
extrude_sheet1 = part.CreateLinearSweepSheet(extrudeParam1,False)
part.SheetAlignNormal(extrude_sheet1,1,0,0)
part.BlankElement(extrude_sheet1,True)
part.SetElementColor(extrude_sheet1,"225","225","225","1")
skt_pl3 = part.CreateSketchPlane("HK.Ax.Deck","","PL,X","0",False,False,False,"","","",True,False)
part.BlankElement(skt_pl3,True)
skt_ln10 = part.CreateSketchLine(skt_pl3,"","作図","15500,31800","15500,-2999.9999999999964",False)
skt_ln11 = part.CreateSketchLine(skt_pl3,"","作図","-15499.999999999996,31800","-15500,-2999.9999999999964",False)
skt_ln12 = part.CreateSketchLine(skt_pl3,"","作図","0,-3000","0,31799.999999999996",False)
skt_layer6 = part.CreateSketchLayer("General.Deck.UpperDeck",skt_pl3)
skt_ln13 = part.CreateSketchLine(skt_pl3,"","General.Deck.UpperDeck","2000,15300","18500,14933.333333333334",False)
skt_ln14 = part.CreateSketchLine(skt_pl3,"","General.Deck.UpperDeck","2000,15300","-2000,15300",False)
skt_ln15 = part.CreateSketchLine(skt_pl3,"","General.Deck.UpperDeck","-2000,15300","-18500,14933.333333333336",False)
skt_layer7 = part.CreateSketchLayer("Casing.Deck.A",skt_pl3)
skt_ln16 = part.CreateSketchLine(skt_pl3,"","Casing.Deck.A","18500,18300","-18500,18300",False)
skt_layer8 = part.CreateSketchLayer("Casing.Deck.B",skt_pl3)
skt_ln17 = part.CreateSketchLine(skt_pl3,"","Casing.Deck.B","18500,21300","-18500,21300",False)
skt_layer9 = part.CreateSketchLayer("Casing.Deck.C",skt_pl3)
skt_ln18 = part.CreateSketchLine(skt_pl3,"","Casing.Deck.C","18500,24300","-18500,24300",False)
skt_layer10 = part.CreateSketchLayer("Casing.Deck.D",skt_pl3)
skt_ln19 = part.CreateSketchLine(skt_pl3,"","Casing.Deck.D","18500,27300","-18500,27300",False)
extrudeParam2 = part.CreateLinearSweepParam()
extrudeParam2.AddProfile(skt_pl3+",Casing.Deck.C")
extrudeParam2.DirectionType="2"
extrudeParam2.DirectionParameter1="50000"
extrudeParam2.DirectionParameter2="10000"
extrudeParam2.SweepDirection="+X"
extrudeParam2.Name="HK.Casing.Deck.C"
extrudeParam2.MaterialName="SS400"
extrudeParam2.IntervalSweep=False
extrude_sheet2 = part.CreateLinearSweepSheet(extrudeParam2,False)
part.SheetAlignNormal(extrude_sheet2,-0,0,1)
part.BlankElement(extrude_sheet2,True)
part.SetElementColor(extrude_sheet2,"225","225","225","1")
extrudeParam3 = part.CreateLinearSweepParam()
extrudeParam3.AddProfile(skt_pl2+",Casing.Fore")
extrudeParam3.DirectionType="2"
extrudeParam3.DirectionParameter1="50000"
extrudeParam3.DirectionParameter2="10000"
extrudeParam3.SweepDirection="+Z"
extrudeParam3.Name="HK.Casing.Wall.Fore"
extrudeParam3.MaterialName="SS400"
extrudeParam3.IntervalSweep=False
extrude_sheet3 = part.CreateLinearSweepSheet(extrudeParam3,False)
part.SheetAlignNormal(extrude_sheet3,1,0,0)
part.BlankElement(extrude_sheet3,True)
part.SetElementColor(extrude_sheet3,"225","225","225","1")
extrudeParam4 = part.CreateLinearSweepParam()
extrudeParam4.AddProfile(skt_pl3+",Casing.Deck.D")
extrudeParam4.DirectionType="2"
extrudeParam4.DirectionParameter1="50000"
extrudeParam4.DirectionParameter2="10000"
extrudeParam4.SweepDirection="+X"
extrudeParam4.Name="HK.Casing.Deck.D"
extrudeParam4.MaterialName="SS400"
extrudeParam4.IntervalSweep=False
extrude_sheet4 = part.CreateLinearSweepSheet(extrudeParam4,False)
part.SheetAlignNormal(extrude_sheet4,-0,0,1)
part.BlankElement(extrude_sheet4,True)
part.SetElementColor(extrude_sheet4,"225","225","225","1")
var_elm1 = part.CreateVariable("Casing.DL02","1600","mm","")
ProfileParam1 = part.CreateProfileParam()
ProfileParam1.DefinitionType=1
ProfileParam1.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfileParam1.AddAttachSurfaces(extrude_sheet4)
ProfileParam1.ProfileName="HK.Casing.Deck.D.DL02P"
ProfileParam1.MaterialName="SS400"
ProfileParam1.FlangeName="HK.Casing.Deck.D.DL02P"
ProfileParam1.FlangeMaterialName="SS400"
ProfileParam1.ProfileType=1201
ProfileParam1.ProfileParams=["200","14","900","10"]
ProfileParam1.Mold="-"
ProfileParam1.ReverseDir=True
ProfileParam1.ReverseAngle=False
ProfileParam1.CalcSnipOnlyAttachLines=False
ProfileParam1.AttachDirMethod=0
ProfileParam1.CCWDefAngle=False
ProfileParam1.AddEnd1Elements(extrude_sheet1)
ProfileParam1.End1Type=1102
ProfileParam1.End1TypeParams=["25","14.999999999999998","0","0"]
ProfileParam1.AddEnd2Elements(extrude_sheet3)
ProfileParam1.End2Type=1102
ProfileParam1.End2TypeParams=["25","14.999999999999998","0","0"]
ProfileParam1.End1ScallopType=1120
ProfileParam1.End1ScallopTypeParams=["50"]
ProfileParam1.End2ScallopType=1120
ProfileParam1.End2ScallopTypeParams=["50"]
profile1 = part.CreateProfile(ProfileParam1,False)
part.BlankElement(profile1[0],True)
part.SetElementColor(profile1[0],"148","0","211","0.39999997615814209")
part.BlankElement(profile1[1],True)
part.SetElementColor(profile1[1],"148","0","211","0.39999997615814209")
ProfileParam2 = part.CreateProfileParam()
ProfileParam2.DefinitionType=1
ProfileParam2.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfileParam2.AddAttachSurfaces(extrude_sheet1)
ProfileParam2.ProfileName="HK.Casing.Wall.Aft.DL02.CDP"
ProfileParam2.MaterialName="SS400"
ProfileParam2.FlangeName="HK.Casing.Wall.Aft.DL02.CDP"
ProfileParam2.FlangeMaterialName="SS400"
ProfileParam2.ProfileType=1201
ProfileParam2.ProfileParams=["150","12","388","10"]
ProfileParam2.Mold="-"
ProfileParam2.ReverseDir=False
ProfileParam2.ReverseAngle=False
ProfileParam2.CalcSnipOnlyAttachLines=False
ProfileParam2.AttachDirMethod=0
ProfileParam2.CCWDefAngle=False
ProfileParam2.AddEnd1Elements(profile1[1])
ProfileParam2.End1Type=1102
ProfileParam2.End1TypeParams=["25","14.999999999999998","0","0"]
ProfileParam2.AddEnd2Elements(extrude_sheet2)
ProfileParam2.End2Type=1103
ProfileParam2.End2TypeParams=["0"]
ProfileParam2.End1ScallopType=1120
ProfileParam2.End1ScallopTypeParams=["50"]
ProfileParam2.End2ScallopType=1120
ProfileParam2.End2ScallopTypeParams=["50"]
profile2 = part.CreateProfile(ProfileParam2,False)
part.BlankElement(profile2[0],True)
part.SetElementColor(profile2[0],"148","0","211","0.38999998569488525")
part.BlankElement(profile2[1],True)
part.SetElementColor(profile2[1],"148","0","211","0.38999998569488525")
extrudeParam5 = part.CreateLinearSweepParam()
extrudeParam5.AddProfile(skt_pl2+",Casing.Side.P")
extrudeParam5.DirectionType="2"
extrudeParam5.DirectionParameter1="50000"
extrudeParam5.DirectionParameter2="10000"
extrudeParam5.SweepDirection="+Z"
extrudeParam5.Name="HK.Casing.Wall.SideP"
extrudeParam5.MaterialName="SS400"
extrudeParam5.IntervalSweep=False
extrude_sheet5 = part.CreateLinearSweepSheet(extrudeParam5,False)
part.SheetAlignNormal(extrude_sheet5,0,-1,0)
part.BlankElement(extrude_sheet5,True)
part.SetElementColor(extrude_sheet5,"225","225","225","1")
var_elm2 = part.CreateVariable("FR12","8170","mm","")
ProfileParam3 = part.CreateProfileParam()
ProfileParam3.DefinitionType=1
ProfileParam3.BasePlane="PL,O,"+var_elm2+","+"X"
ProfileParam3.AddAttachSurfaces(extrude_sheet5)
ProfileParam3.ProfileName="HK.Casing.Wall.Side.FR12.CDP"
ProfileParam3.MaterialName="SS400"
ProfileParam3.ProfileType=1002
ProfileParam3.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfileParam3.Mold="+"
ProfileParam3.ReverseDir=False
ProfileParam3.ReverseAngle=True
ProfileParam3.CalcSnipOnlyAttachLines=False
ProfileParam3.AttachDirMethod=0
ProfileParam3.CCWDefAngle=False
ProfileParam3.AddEnd1Elements(extrude_sheet4)
ProfileParam3.End1Type=1102
ProfileParam3.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam3.AddEnd2Elements(extrude_sheet2)
ProfileParam3.End2Type=1102
ProfileParam3.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam3.End1ScallopType=1121
ProfileParam3.End1ScallopTypeParams=["35","40"]
ProfileParam3.End2ScallopType=1121
ProfileParam3.End2ScallopTypeParams=["35","40"]
profile3 = part.CreateProfile(ProfileParam3,False)
part.BlankElement(profile3[0],True)
part.SetElementColor(profile3[0],"255","0","0","0.19999998807907104")
skt_pl4 = part.CreateSketchPlane("HK.Az.Deck.D","","PL,Z","0",False,False,False,"","","",False,False)
part.BlankElement(skt_pl4,True)
skt_layer11 = part.CreateSketchLayer("Edge00",skt_pl4)
skt_ln20 = part.CreateSketchLine(skt_pl4,"","Edge00","11405.000000000002,4835","3984.9999999999995,4835",False)
skt_ln21 = part.CreateSketchLine(skt_pl4,"","Edge00","11405.000000000002,-4835","11405.000000000002,4835",False)
skt_ln22 = part.CreateSketchLine(skt_pl4,"","Edge00","3984.9999999999995,-4835","11405.000000000002,-4835",False)
skt_ln23 = part.CreateSketchLine(skt_pl4,"","Edge00","3984.9999999999995,4835","3984.9999999999995,-4835",False)
skt_layer12 = part.CreateSketchLayer("Edge01",skt_pl4)
skt_arc1 = part.CreateSketchArc(skt_pl4,"","Edge01","6345.0000000000009,1195.0000000000002","6345,1495.0000000000002","6045.0000000000009,1195",True,False)
skt_ln24 = part.CreateSketchLine(skt_pl4,"","Edge01","8580,1495","6345,1495",False)
skt_arc2 = part.CreateSketchArc(skt_pl4,"","Edge01","8580,1195","8880,1195.0000000000002","8580,1495.0000000000007",True,False)
skt_ln25 = part.CreateSketchLine(skt_pl4,"","Edge01","8880,-1195","8880,1195.0000000000005",False)
skt_arc3 = part.CreateSketchArc(skt_pl4,"","Edge01","8580,-1195.0000000000002","8580,-1495.0000000000002","8880,-1195",True,False)
skt_ln26 = part.CreateSketchLine(skt_pl4,"","Edge01","6345,-1495","8580,-1495",False)
skt_arc4 = part.CreateSketchArc(skt_pl4,"","Edge01","6345.0000000000009,-1195","6045.0000000000009,-1195.0000000000002","6345,-1494.9999999999998",True,False)
skt_ln27 = part.CreateSketchLine(skt_pl4,"","Edge01","6045,1195","6045,-1195.0000000000005",False)
var_elm3 = part.CreateVariable("Casing.DL05","4000","mm","")
ProfileParam4 = part.CreateProfileParam()
ProfileParam4.DefinitionType=1
ProfileParam4.BasePlane="PL,O,"+var_elm3+","+"Y"
ProfileParam4.AddAttachSurfaces(extrude_sheet4)
ProfileParam4.ProfileName="HK.Casing.Deck.D.DL05P"
ProfileParam4.MaterialName="SS400"
ProfileParam4.ProfileType=1002
ProfileParam4.ProfileParams=["125","75","7","10","5"]
ProfileParam4.Mold="+"
ProfileParam4.ReverseDir=True
ProfileParam4.ReverseAngle=True
ProfileParam4.CalcSnipOnlyAttachLines=False
ProfileParam4.AttachDirMethod=0
ProfileParam4.CCWDefAngle=False
ProfileParam4.AddEnd1Elements(extrude_sheet1)
ProfileParam4.End1Type=1102
ProfileParam4.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam4.AddEnd2Elements(extrude_sheet3)
ProfileParam4.End2Type=1102
ProfileParam4.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam4.End1ScallopType=1120
ProfileParam4.End1ScallopTypeParams=["50"]
ProfileParam4.End2ScallopType=1120
ProfileParam4.End2ScallopTypeParams=["50"]
profile4 = part.CreateProfile(ProfileParam4,False)
part.BlankElement(profile4[0],True)
part.SetElementColor(profile4[0],"255","0","0","0.19999998807907104")
var_elm4 = part.CreateVariable("FR11","7370","mm","")
ProfileParam5 = part.CreateProfileParam()
ProfileParam5.DefinitionType=1
ProfileParam5.BasePlane="PL,O,"+var_elm4+","+"X"
ProfileParam5.AddAttachSurfaces(extrude_sheet5)
ProfileParam5.ProfileName="HK.Casing.Wall.Side.FR11.CDP"
ProfileParam5.MaterialName="SS400"
ProfileParam5.ProfileType=1002
ProfileParam5.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfileParam5.Mold="+"
ProfileParam5.ReverseDir=False
ProfileParam5.ReverseAngle=True
ProfileParam5.CalcSnipOnlyAttachLines=False
ProfileParam5.AttachDirMethod=0
ProfileParam5.CCWDefAngle=False
ProfileParam5.AddEnd1Elements(extrude_sheet4)
ProfileParam5.End1Type=1102
ProfileParam5.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam5.AddEnd2Elements(extrude_sheet2)
ProfileParam5.End2Type=1102
ProfileParam5.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam5.End1ScallopType=1121
ProfileParam5.End1ScallopTypeParams=["35","40"]
ProfileParam5.End2ScallopType=1121
ProfileParam5.End2ScallopTypeParams=["35","40"]
profile5 = part.CreateProfile(ProfileParam5,False)
part.BlankElement(profile5[0],True)
part.SetElementColor(profile5[0],"255","0","0","0.19999998807907104")
separated_bodies1 = part.BodyDivideByCurves("Separe body by curves11",profile5[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies1[0],"255","0","0","0.19999998807907104")
extrudeParam6 = part.CreateLinearSweepParam()
extrudeParam6.AddProfile(skt_pl2+",Casing.Side.S")
extrudeParam6.DirectionType="2"
extrudeParam6.DirectionParameter1="50000"
extrudeParam6.DirectionParameter2="10000"
extrudeParam6.SweepDirection="+Z"
extrudeParam6.Name="HK.Casing.Wall.SideS"
extrudeParam6.MaterialName="SS400"
extrudeParam6.IntervalSweep=False
extrude_sheet6 = part.CreateLinearSweepSheet(extrudeParam6,False)
part.SheetAlignNormal(extrude_sheet6,0,-1,0)
part.BlankElement(extrude_sheet6,True)
part.SetElementColor(extrude_sheet6,"225","225","225","1")
solid1 = part.CreateSolid("HK.Casing.Wall.Aft.CD","","SS400")
part.BlankElement(solid1,True)
part.SetElementColor(solid1,"139","69","19","0.79999995231628418")
thicken1 = part.CreateThicken("厚み付け11",solid1,"+",[extrude_sheet1],"-","10","0","0",False,False)
extrudeParam7 = part.CreateLinearSweepParam()
extrudeParam7.Name="積-押し出し19"
extrudeParam7.AddProfile(extrude_sheet5)
extrudeParam7.DirectionType="R"
extrudeParam7.DirectionParameter1="50000"
extrudeParam7.SweepDirection="+Y"
extrudeParam7.RefByGeometricMethod=False
extrude1 = part.CreateLinearSweep(solid1,"*",extrudeParam7,False)
extrudeParam8 = part.CreateLinearSweepParam()
extrudeParam8.Name="積-押し出し20"
extrudeParam8.AddProfile(extrude_sheet6)
extrudeParam8.DirectionType="N"
extrudeParam8.DirectionParameter1="50000"
extrudeParam8.SweepDirection="+Y"
extrudeParam8.RefByGeometricMethod=False
extrude2 = part.CreateLinearSweep(solid1,"*",extrudeParam8,False)
extrudeParam9 = part.CreateLinearSweepParam()
extrudeParam9.Name="積-押し出し21"
extrudeParam9.AddProfile(extrude_sheet4)
extrudeParam9.DirectionType="R"
extrudeParam9.DirectionParameter1="50000"
extrudeParam9.SweepDirection="+Z"
extrudeParam9.RefByGeometricMethod=False
extrude3 = part.CreateLinearSweep(solid1,"*",extrudeParam9,False)
var_elm5 = part.CreateVariable("FR15","10570","mm","")
ProfileParam6 = part.CreateProfileParam()
ProfileParam6.DefinitionType=1
ProfileParam6.BasePlane="PL,O,"+var_elm5+","+"X"
ProfileParam6.AddAttachSurfaces(extrude_sheet5)
ProfileParam6.ProfileName="HK.Casing.Wall.Side.FR15.CDP"
ProfileParam6.MaterialName="SS400"
ProfileParam6.ProfileType=1002
ProfileParam6.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfileParam6.Mold="+"
ProfileParam6.ReverseDir=False
ProfileParam6.ReverseAngle=True
ProfileParam6.CalcSnipOnlyAttachLines=False
ProfileParam6.AttachDirMethod=0
ProfileParam6.CCWDefAngle=False
ProfileParam6.AddEnd1Elements(extrude_sheet4)
ProfileParam6.End1Type=1102
ProfileParam6.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam6.AddEnd2Elements(extrude_sheet2)
ProfileParam6.End2Type=1102
ProfileParam6.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam6.End1ScallopType=1121
ProfileParam6.End1ScallopTypeParams=["35","40"]
ProfileParam6.End2ScallopType=1121
ProfileParam6.End2ScallopTypeParams=["35","40"]
profile6 = part.CreateProfile(ProfileParam6,False)
part.BlankElement(profile6[0],True)
part.SetElementColor(profile6[0],"255","0","0","0.19999998807907104")
var_elm6 = part.CreateVariable("Casing.DL04","3200","mm","")
ProfileParam7 = part.CreateProfileParam()
ProfileParam7.DefinitionType=1
ProfileParam7.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfileParam7.AddAttachSurfaces(extrude_sheet4)
ProfileParam7.ProfileName="HK.Casing.Deck.D.DL04P"
ProfileParam7.MaterialName="SS400"
ProfileParam7.ProfileType=1002
ProfileParam7.ProfileParams=["125","75","7","10","5"]
ProfileParam7.Mold="+"
ProfileParam7.ReverseDir=True
ProfileParam7.ReverseAngle=True
ProfileParam7.CalcSnipOnlyAttachLines=False
ProfileParam7.AttachDirMethod=0
ProfileParam7.CCWDefAngle=False
ProfileParam7.AddEnd1Elements(extrude_sheet1)
ProfileParam7.End1Type=1102
ProfileParam7.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam7.AddEnd2Elements(extrude_sheet3)
ProfileParam7.End2Type=1102
ProfileParam7.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam7.End1ScallopType=1120
ProfileParam7.End1ScallopTypeParams=["50"]
ProfileParam7.End2ScallopType=1120
ProfileParam7.End2ScallopTypeParams=["50"]
profile7 = part.CreateProfile(ProfileParam7,False)
part.BlankElement(profile7[0],True)
part.SetElementColor(profile7[0],"255","0","0","0.19999998807907104")
ProfileParam8 = part.CreateProfileParam()
ProfileParam8.DefinitionType=1
ProfileParam8.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfileParam8.AddAttachSurfaces(extrude_sheet1)
ProfileParam8.ProfileName="HK.Casing.Wall.Aft.DL04.CDP"
ProfileParam8.MaterialName="SS400"
ProfileParam8.ProfileType=1002
ProfileParam8.ProfileParams=["125","75","7","10","5"]
ProfileParam8.Mold="+"
ProfileParam8.ReverseDir=False
ProfileParam8.ReverseAngle=True
ProfileParam8.CalcSnipOnlyAttachLines=False
ProfileParam8.AttachDirMethod=0
ProfileParam8.CCWDefAngle=False
ProfileParam8.AddEnd1Elements(profile7[0])
ProfileParam8.End1Type=1102
ProfileParam8.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam8.AddEnd2Elements(extrude_sheet2)
ProfileParam8.End2Type=1102
ProfileParam8.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam8.End1ScallopType=1120
ProfileParam8.End1ScallopTypeParams=["50"]
ProfileParam8.End2ScallopType=1120
ProfileParam8.End2ScallopTypeParams=["50"]
profile8 = part.CreateProfile(ProfileParam8,False)
part.BlankElement(profile8[0],True)
part.SetElementColor(profile8[0],"255","0","0","0.19999998807907104")
solid2 = part.CreateSolid("HK.Casing.Wall.Fore.CD","","SS400")
part.BlankElement(solid2,True)
part.SetElementColor(solid2,"139","69","19","0.79999995231628418")
thicken2 = part.CreateThicken("厚み付け15",solid2,"+",[extrude_sheet3],"+","10","0","0",False,False)
extrudeParam10 = part.CreateLinearSweepParam()
extrudeParam10.Name="積-押し出し35"
extrudeParam10.AddProfile(extrude_sheet5)
extrudeParam10.DirectionType="R"
extrudeParam10.DirectionParameter1="50000"
extrudeParam10.SweepDirection="+Y"
extrudeParam10.RefByGeometricMethod=False
extrude4 = part.CreateLinearSweep(solid2,"*",extrudeParam10,False)
extrudeParam11 = part.CreateLinearSweepParam()
extrudeParam11.Name="積-押し出し36"
extrudeParam11.AddProfile(extrude_sheet6)
extrudeParam11.DirectionType="N"
extrudeParam11.DirectionParameter1="50000"
extrudeParam11.SweepDirection="+Y"
extrudeParam11.RefByGeometricMethod=False
extrude5 = part.CreateLinearSweep(solid2,"*",extrudeParam11,False)
extrudeParam12 = part.CreateLinearSweepParam()
extrudeParam12.Name="積-押し出し37"
extrudeParam12.AddProfile(extrude_sheet4)
extrudeParam12.DirectionType="R"
extrudeParam12.DirectionParameter1="50000"
extrudeParam12.SweepDirection="+Z"
extrudeParam12.RefByGeometricMethod=False
extrude6 = part.CreateLinearSweep(solid2,"*",extrudeParam12,False)
extrudeParam13 = part.CreateLinearSweepParam()
extrudeParam13.Name="積-押し出し38"
extrudeParam13.AddProfile(extrude_sheet2)
extrudeParam13.DirectionType="N"
extrudeParam13.DirectionParameter1="50000"
extrudeParam13.SweepDirection="+Z"
extrudeParam13.RefByGeometricMethod=False
extrude7 = part.CreateLinearSweep(solid2,"*",extrudeParam13,False)
var_elm7 = part.CreateVariable("FR13","8970","mm","")
ProfileParam9 = part.CreateProfileParam()
ProfileParam9.DefinitionType=1
ProfileParam9.BasePlane="PL,O,"+var_elm7+","+"X"
ProfileParam9.AddAttachSurfaces(extrude_sheet4)
ProfileParam9.ProfileName="HK.Casing.Deck.D.FR13P"
ProfileParam9.MaterialName="SS400"
ProfileParam9.ProfileType=1003
ProfileParam9.ProfileParams=["300","90","11","16","19","9.5"]
ProfileParam9.Mold="+"
ProfileParam9.ReverseDir=True
ProfileParam9.ReverseAngle=False
ProfileParam9.CalcSnipOnlyAttachLines=False
ProfileParam9.AttachDirMethod=0
ProfileParam9.CCWDefAngle=False
ProfileParam9.AddEnd1Elements(profile1[0])
ProfileParam9.End1Type=1102
ProfileParam9.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam9.AddEnd2Elements(extrude_sheet5)
ProfileParam9.End2Type=1102
ProfileParam9.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam9.End1ScallopType=1120
ProfileParam9.End1ScallopTypeParams=["50"]
ProfileParam9.End2ScallopType=1120
ProfileParam9.End2ScallopTypeParams=["50"]
profile9 = part.CreateProfile(ProfileParam9,False)
part.BlankElement(profile9[0],True)
part.SetElementColor(profile9[0],"148","0","211","0.39999997615814209")
separated_bodies2 = part.BodyDivideByCurves("Separe body by curves21",profile9[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies2[0],"148","0","211","0.39999997615814209")
ProfileParam10 = part.CreateProfileParam()
ProfileParam10.DefinitionType=1
ProfileParam10.BasePlane="PL,O,"+var_elm3+","+"Y"
ProfileParam10.AddAttachSurfaces(extrude_sheet1)
ProfileParam10.ProfileName="HK.Casing.Wall.Aft.DL05.CDP"
ProfileParam10.MaterialName="SS400"
ProfileParam10.ProfileType=1002
ProfileParam10.ProfileParams=["125","75","7","10","5"]
ProfileParam10.Mold="+"
ProfileParam10.ReverseDir=False
ProfileParam10.ReverseAngle=True
ProfileParam10.CalcSnipOnlyAttachLines=False
ProfileParam10.AttachDirMethod=0
ProfileParam10.CCWDefAngle=False
ProfileParam10.AddEnd1Elements(profile4[0])
ProfileParam10.End1Type=1102
ProfileParam10.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam10.AddEnd2Elements(extrude_sheet2)
ProfileParam10.End2Type=1102
ProfileParam10.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam10.End1ScallopType=1120
ProfileParam10.End1ScallopTypeParams=["50"]
ProfileParam10.End2ScallopType=1120
ProfileParam10.End2ScallopTypeParams=["50"]
profile10 = part.CreateProfile(ProfileParam10,False)
part.BlankElement(profile10[0],True)
part.SetElementColor(profile10[0],"255","0","0","0.19999998807907104")
separated_bodies3 = part.BodyDivideByCurves("Separe body by curves40",profile10[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies3[0],"255","0","0","0.19999998807907104")
mirror_copied1 = part.MirrorCopy([profile1[0]],"PL,Y","")
part.BlankElement(mirror_copied1[0],True)
part.SetElementColor(mirror_copied1[0],"148","0","211","0.39999997615814209")
ProfileParam11 = part.CreateProfileParam()
ProfileParam11.DefinitionType=1
ProfileParam11.BasePlane="PL,O,"+var_elm7+","+"X"
ProfileParam11.AddAttachSurfaces(extrude_sheet4)
ProfileParam11.ProfileName="HK.Casing.Deck.D.FR13C"
ProfileParam11.MaterialName="SS400"
ProfileParam11.ProfileType=1003
ProfileParam11.ProfileParams=["300","90","11","16","19","9.5"]
ProfileParam11.Mold="+"
ProfileParam11.ReverseDir=True
ProfileParam11.ReverseAngle=False
ProfileParam11.CalcSnipOnlyAttachLines=False
ProfileParam11.AttachDirMethod=0
ProfileParam11.CCWDefAngle=False
ProfileParam11.AddEnd1Elements(mirror_copied1[0])
ProfileParam11.End1Type=1102
ProfileParam11.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam11.AddEnd2Elements(profile1[0])
ProfileParam11.End2Type=1102
ProfileParam11.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam11.End1ScallopType=1120
ProfileParam11.End1ScallopTypeParams=["50"]
ProfileParam11.End2ScallopType=1120
ProfileParam11.End2ScallopTypeParams=["50"]
profile11 = part.CreateProfile(ProfileParam11,False)
part.BlankElement(profile11[0],True)
part.SetElementColor(profile11[0],"148","0","211","0.39999997615814209")
var_elm8 = part.CreateVariable("Casing.DL01","800","mm","")
ProfileParam12 = part.CreateProfileParam()
ProfileParam12.DefinitionType=1
ProfileParam12.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfileParam12.AddAttachSurfaces(extrude_sheet4)
ProfileParam12.ProfileName="HK.Casing.Deck.D.DL01.FP"
ProfileParam12.MaterialName="SS400"
ProfileParam12.ProfileType=1002
ProfileParam12.ProfileParams=["125","75","7","10","5"]
ProfileParam12.Mold="+"
ProfileParam12.ReverseDir=True
ProfileParam12.ReverseAngle=True
ProfileParam12.CalcSnipOnlyAttachLines=False
ProfileParam12.AttachDirMethod=0
ProfileParam12.CCWDefAngle=False
ProfileParam12.AddEnd1Elements(profile11[0])
ProfileParam12.End1Type=1102
ProfileParam12.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam12.AddEnd2Elements(extrude_sheet3)
ProfileParam12.End2Type=1102
ProfileParam12.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam12.End1ScallopType=1121
ProfileParam12.End1ScallopTypeParams=["25","40"]
ProfileParam12.End2ScallopType=1121
ProfileParam12.End2ScallopTypeParams=["25","40"]
profile12 = part.CreateProfile(ProfileParam12,False)
part.BlankElement(profile12[0],True)
part.SetElementColor(profile12[0],"255","0","0","0.19999998807907104")
separated_bodies4 = part.BodyDivideByCurves("Separe body by curves3",profile12[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies4[0],"255","0","0","0.19999998807907104")
solid3 = part.CreateSolid("HK.Casing.Wall.Side.CDP","","SS400")
part.BlankElement(solid3,True)
part.SetElementColor(solid3,"139","69","19","0.79999995231628418")
thicken3 = part.CreateThicken("厚み付け7",solid3,"+",[extrude_sheet5],"-","10","0","0",False,False)
extrudeParam14 = part.CreateLinearSweepParam()
extrudeParam14.Name="積-押し出し7"
extrudeParam14.AddProfile(skt_pl4+",Edge00")
extrudeParam14.DirectionType="N"
extrudeParam14.DirectionParameter1="50000"
extrudeParam14.SweepDirection="+Z"
extrudeParam14.RefByGeometricMethod=False
extrude8 = part.CreateLinearSweep(solid3,"*",extrudeParam14,False)
extrudeParam15 = part.CreateLinearSweepParam()
extrudeParam15.Name="積-押し出し8"
extrudeParam15.AddProfile(extrude_sheet4)
extrudeParam15.DirectionType="R"
extrudeParam15.DirectionParameter1="50000"
extrudeParam15.SweepDirection="+Z"
extrudeParam15.RefByGeometricMethod=False
extrude9 = part.CreateLinearSweep(solid3,"*",extrudeParam15,False)
extrudeParam16 = part.CreateLinearSweepParam()
extrudeParam16.Name="積-押し出し9"
extrudeParam16.AddProfile(extrude_sheet2)
extrudeParam16.DirectionType="N"
extrudeParam16.DirectionParameter1="50000"
extrudeParam16.SweepDirection="+Z"
extrudeParam16.RefByGeometricMethod=False
extrude10 = part.CreateLinearSweep(solid3,"*",extrudeParam16,False)
separated_bodies5 = part.BodyDivideByCurves("Separe body by curves27",solid3,[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies5[0],"139","69","19","0.79999995231628418")
separated_bodies6 = part.BodyDivideByCurves("Separe body by curves19",profile1[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies6[0],"148","0","211","0.39999997615814209")
var_elm9 = part.CreateVariable("FR10","6700","mm","")
ProfileParam13 = part.CreateProfileParam()
ProfileParam13.DefinitionType=1
ProfileParam13.BasePlane="PL,O,"+var_elm9+","+"X"
ProfileParam13.AddAttachSurfaces(extrude_sheet5)
ProfileParam13.ProfileName="HK.Casing.Wall.Side.FR10.CDP"
ProfileParam13.MaterialName="SS400"
ProfileParam13.ProfileType=1002
ProfileParam13.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfileParam13.Mold="+"
ProfileParam13.ReverseDir=False
ProfileParam13.ReverseAngle=True
ProfileParam13.CalcSnipOnlyAttachLines=False
ProfileParam13.AttachDirMethod=0
ProfileParam13.CCWDefAngle=False
ProfileParam13.AddEnd1Elements(extrude_sheet4)
ProfileParam13.End1Type=1102
ProfileParam13.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam13.AddEnd2Elements(extrude_sheet2)
ProfileParam13.End2Type=1102
ProfileParam13.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam13.End1ScallopType=1121
ProfileParam13.End1ScallopTypeParams=["35","40"]
ProfileParam13.End2ScallopType=1121
ProfileParam13.End2ScallopTypeParams=["35","40"]
profile13 = part.CreateProfile(ProfileParam13,False)
part.BlankElement(profile13[0],True)
part.SetElementColor(profile13[0],"255","0","0","0.19999998807907104")
separated_bodies7 = part.BodyDivideByCurves("Separe body by curves14",profile13[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies7[0],"255","0","0","0.19999998807907104")
var_elm10 = part.CreateVariable("FR8","5360","mm","")
ProfileParam14 = part.CreateProfileParam()
ProfileParam14.DefinitionType=1
ProfileParam14.BasePlane="PL,O,"+var_elm10+","+"X"
ProfileParam14.AddAttachSurfaces(extrude_sheet5)
ProfileParam14.ProfileName="HK.Casing.Wall.Side.FR08.CDP"
ProfileParam14.MaterialName="SS400"
ProfileParam14.ProfileType=1002
ProfileParam14.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfileParam14.Mold="+"
ProfileParam14.ReverseDir=False
ProfileParam14.ReverseAngle=True
ProfileParam14.CalcSnipOnlyAttachLines=False
ProfileParam14.AttachDirMethod=0
ProfileParam14.CCWDefAngle=False
ProfileParam14.AddEnd1Elements(extrude_sheet4)
ProfileParam14.End1Type=1102
ProfileParam14.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam14.AddEnd2Elements(extrude_sheet2)
ProfileParam14.End2Type=1102
ProfileParam14.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam14.End1ScallopType=1121
ProfileParam14.End1ScallopTypeParams=["35","40"]
ProfileParam14.End2ScallopType=1121
ProfileParam14.End2ScallopTypeParams=["35","40"]
profile14 = part.CreateProfile(ProfileParam14,False)
part.BlankElement(profile14[0],True)
part.SetElementColor(profile14[0],"255","0","0","0.19999998807907104")
separated_bodies8 = part.BodyDivideByCurves("Separe body by curves7",profile14[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies8[0],"255","0","0","0.19999998807907104")
ProfileParam15 = part.CreateProfileParam()
ProfileParam15.DefinitionType=1
ProfileParam15.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfileParam15.AddAttachSurfaces(extrude_sheet3)
ProfileParam15.ProfileName="HK.Casing.Wall.Fore.DL01.CDP"
ProfileParam15.MaterialName="SS400"
ProfileParam15.ProfileType=1002
ProfileParam15.ProfileParams=["125","75","7","10","5"]
ProfileParam15.Mold="+"
ProfileParam15.ReverseDir=True
ProfileParam15.ReverseAngle=True
ProfileParam15.CalcSnipOnlyAttachLines=False
ProfileParam15.AttachDirMethod=0
ProfileParam15.CCWDefAngle=False
ProfileParam15.AddEnd1Elements(profile12[0])
ProfileParam15.End1Type=1102
ProfileParam15.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam15.AddEnd2Elements(extrude_sheet2)
ProfileParam15.End2Type=1102
ProfileParam15.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam15.End1ScallopType=1120
ProfileParam15.End1ScallopTypeParams=["50"]
ProfileParam15.End2ScallopType=1120
ProfileParam15.End2ScallopTypeParams=["50"]
profile15 = part.CreateProfile(ProfileParam15,False)
part.BlankElement(profile15[0],True)
part.SetElementColor(profile15[0],"255","0","0","0.19999998807907104")
separated_bodies9 = part.BodyDivideByCurves("Separe body by curves37",profile15[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies9[0],"255","0","0","0.19999998807907104")
var_elm11 = part.CreateVariable("FR9","6030","mm","")
ProfileParam16 = part.CreateProfileParam()
ProfileParam16.DefinitionType=1
ProfileParam16.BasePlane="PL,O,"+var_elm11+","+"X"
ProfileParam16.AddAttachSurfaces(extrude_sheet4)
ProfileParam16.ProfileName="HK.Casing.Deck.D.FR09C"
ProfileParam16.MaterialName="SS400"
ProfileParam16.ProfileType=1003
ProfileParam16.ProfileParams=["300","90","11","16","19","9.5"]
ProfileParam16.Mold="+"
ProfileParam16.ReverseDir=True
ProfileParam16.ReverseAngle=False
ProfileParam16.CalcSnipOnlyAttachLines=False
ProfileParam16.AttachDirMethod=0
ProfileParam16.CCWDefAngle=False
ProfileParam16.AddEnd1Elements(mirror_copied1[0])
ProfileParam16.End1Type=1102
ProfileParam16.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam16.AddEnd2Elements(profile1[0])
ProfileParam16.End2Type=1102
ProfileParam16.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam16.End1ScallopType=1120
ProfileParam16.End1ScallopTypeParams=["50"]
ProfileParam16.End2ScallopType=1120
ProfileParam16.End2ScallopTypeParams=["50"]
profile16 = part.CreateProfile(ProfileParam16,False)
part.BlankElement(profile16[0],True)
part.SetElementColor(profile16[0],"148","0","211","0.39999997615814209")
ProfileParam17 = part.CreateProfileParam()
ProfileParam17.DefinitionType=1
ProfileParam17.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfileParam17.AddAttachSurfaces(extrude_sheet4)
ProfileParam17.ProfileName="HK.Casing.Deck.D.DL01.AP"
ProfileParam17.MaterialName="SS400"
ProfileParam17.ProfileType=1002
ProfileParam17.ProfileParams=["125","75","7","10","5"]
ProfileParam17.Mold="+"
ProfileParam17.ReverseDir=True
ProfileParam17.ReverseAngle=True
ProfileParam17.CalcSnipOnlyAttachLines=False
ProfileParam17.AttachDirMethod=0
ProfileParam17.CCWDefAngle=False
ProfileParam17.AddEnd1Elements(extrude_sheet1)
ProfileParam17.End1Type=1102
ProfileParam17.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam17.AddEnd2Elements(profile16[0])
ProfileParam17.End2Type=1102
ProfileParam17.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam17.End1ScallopType=1120
ProfileParam17.End1ScallopTypeParams=["50"]
ProfileParam17.End2ScallopType=1120
ProfileParam17.End2ScallopTypeParams=["50"]
profile17 = part.CreateProfile(ProfileParam17,False)
part.BlankElement(profile17[0],True)
part.SetElementColor(profile17[0],"255","0","0","0.19999998807907104")
ProfileParam18 = part.CreateProfileParam()
ProfileParam18.DefinitionType=1
ProfileParam18.BasePlane="PL,O,"+var_elm8+","+"Y"
ProfileParam18.AddAttachSurfaces(extrude_sheet1)
ProfileParam18.ProfileName="HK.Casing.Wall.Aft.DL01.CDP"
ProfileParam18.MaterialName="SS400"
ProfileParam18.ProfileType=1002
ProfileParam18.ProfileParams=["125","75","7","10","5"]
ProfileParam18.Mold="+"
ProfileParam18.ReverseDir=False
ProfileParam18.ReverseAngle=True
ProfileParam18.CalcSnipOnlyAttachLines=False
ProfileParam18.AttachDirMethod=0
ProfileParam18.CCWDefAngle=False
ProfileParam18.AddEnd1Elements(profile17[0])
ProfileParam18.End1Type=1102
ProfileParam18.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam18.AddEnd2Elements(extrude_sheet2)
ProfileParam18.End2Type=1102
ProfileParam18.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam18.End1ScallopType=1120
ProfileParam18.End1ScallopTypeParams=["50"]
ProfileParam18.End2ScallopType=1120
ProfileParam18.End2ScallopTypeParams=["50"]
profile18 = part.CreateProfile(ProfileParam18,False)
part.BlankElement(profile18[0],True)
part.SetElementColor(profile18[0],"255","0","0","0.19999998807907104")
separated_bodies10 = part.BodyDivideByCurves("Separe body by curves39",profile18[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies10[0],"255","0","0","0.19999998807907104")
separated_bodies11 = part.BodyDivideByCurves("Separe body by curves54",profile2[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies11[0],"148","0","211","0.38999998569488525")
ProfileParam19 = part.CreateProfileParam()
ProfileParam19.DefinitionType=1
ProfileParam19.BasePlane="PL,O,"+var_elm6+","+"Y"
ProfileParam19.AddAttachSurfaces(extrude_sheet3)
ProfileParam19.ProfileName="HK.Casing.Wall.Fore.DL04.CDP"
ProfileParam19.MaterialName="SS400"
ProfileParam19.ProfileType=1002
ProfileParam19.ProfileParams=["125","75","7","10","5"]
ProfileParam19.Mold="+"
ProfileParam19.ReverseDir=True
ProfileParam19.ReverseAngle=True
ProfileParam19.CalcSnipOnlyAttachLines=False
ProfileParam19.AttachDirMethod=0
ProfileParam19.CCWDefAngle=False
ProfileParam19.AddEnd1Elements(profile7[0])
ProfileParam19.End1Type=1102
ProfileParam19.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam19.AddEnd2Elements(extrude_sheet2)
ProfileParam19.End2Type=1102
ProfileParam19.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam19.End1ScallopType=1120
ProfileParam19.End1ScallopTypeParams=["50"]
ProfileParam19.End2ScallopType=1120
ProfileParam19.End2ScallopTypeParams=["50"]
profile19 = part.CreateProfile(ProfileParam19,False)
part.BlankElement(profile19[0],True)
part.SetElementColor(profile19[0],"255","0","0","0.19999998807907104")
separated_bodies12 = part.BodyDivideByCurves("Separe body by curves44",profile19[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies12[0],"255","0","0","0.19999998807907104")
ProfileParam20 = part.CreateProfileParam()
ProfileParam20.DefinitionType=1
ProfileParam20.BasePlane="PL,O,"+var_elm7+","+"X"
ProfileParam20.AddAttachSurfaces(extrude_sheet5)
ProfileParam20.ProfileName="HK.Casing.Wall.Side.FR13.CDP"
ProfileParam20.MaterialName="SS400"
ProfileParam20.ProfileType=1003
ProfileParam20.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfileParam20.Mold="+"
ProfileParam20.ReverseDir=False
ProfileParam20.ReverseAngle=True
ProfileParam20.CalcSnipOnlyAttachLines=False
ProfileParam20.AttachDirMethod=0
ProfileParam20.CCWDefAngle=False
ProfileParam20.AddEnd1Elements(profile9[0])
ProfileParam20.End1Type=1102
ProfileParam20.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam20.AddEnd2Elements(extrude_sheet2)
ProfileParam20.End2Type=1103
ProfileParam20.End2TypeParams=["0"]
ProfileParam20.End1ScallopType=1120
ProfileParam20.End1ScallopTypeParams=["50"]
ProfileParam20.End2ScallopType=1120
ProfileParam20.End2ScallopTypeParams=["50"]
profile20 = part.CreateProfile(ProfileParam20,False)
part.BlankElement(profile20[0],True)
part.SetElementColor(profile20[0],"148","0","211","0.39999997615814209")
separated_bodies13 = part.BodyDivideByCurves("Separe body by curves49",profile20[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies13[0],"148","0","211","0.39999997615814209")
var_elm12 = part.CreateVariable("Casing.DL03","2400","mm","")
ProfileParam21 = part.CreateProfileParam()
ProfileParam21.DefinitionType=1
ProfileParam21.BasePlane="PL,O,"+var_elm12+","+"Y"
ProfileParam21.AddAttachSurfaces(extrude_sheet4)
ProfileParam21.ProfileName="HK.Casing.Deck.D.DL03P"
ProfileParam21.MaterialName="SS400"
ProfileParam21.ProfileType=1002
ProfileParam21.ProfileParams=["125","75","7","10","5"]
ProfileParam21.Mold="+"
ProfileParam21.ReverseDir=True
ProfileParam21.ReverseAngle=True
ProfileParam21.CalcSnipOnlyAttachLines=False
ProfileParam21.AttachDirMethod=0
ProfileParam21.CCWDefAngle=False
ProfileParam21.AddEnd1Elements(extrude_sheet1)
ProfileParam21.End1Type=1102
ProfileParam21.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam21.AddEnd2Elements(extrude_sheet3)
ProfileParam21.End2Type=1102
ProfileParam21.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam21.End1ScallopType=1120
ProfileParam21.End1ScallopTypeParams=["50"]
ProfileParam21.End2ScallopType=1120
ProfileParam21.End2ScallopTypeParams=["50"]
profile21 = part.CreateProfile(ProfileParam21,False)
part.BlankElement(profile21[0],True)
part.SetElementColor(profile21[0],"255","0","0","0.19999998807907104")
separated_bodies14 = part.BodyDivideByCurves("Separe body by curves20",profile21[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies14[0],"255","0","0","0.19999998807907104")
separated_bodies15 = part.BodyDivideByCurves("Separe body by curves23",profile4[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies15[0],"255","0","0","0.19999998807907104")
var_elm13 = part.CreateVariable("FR14","9770","mm","")
ProfileParam22 = part.CreateProfileParam()
ProfileParam22.DefinitionType=1
ProfileParam22.BasePlane="PL,O,"+var_elm13+","+"X"
ProfileParam22.AddAttachSurfaces(extrude_sheet5)
ProfileParam22.ProfileName="HK.Casing.Wall.Side.FR14.CDP"
ProfileParam22.MaterialName="SS400"
ProfileParam22.ProfileType=1002
ProfileParam22.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfileParam22.Mold="+"
ProfileParam22.ReverseDir=False
ProfileParam22.ReverseAngle=True
ProfileParam22.CalcSnipOnlyAttachLines=False
ProfileParam22.AttachDirMethod=0
ProfileParam22.CCWDefAngle=False
ProfileParam22.AddEnd1Elements(extrude_sheet4)
ProfileParam22.End1Type=1102
ProfileParam22.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam22.AddEnd2Elements(extrude_sheet2)
ProfileParam22.End2Type=1102
ProfileParam22.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam22.End1ScallopType=1121
ProfileParam22.End1ScallopTypeParams=["35","40"]
ProfileParam22.End2ScallopType=1121
ProfileParam22.End2ScallopTypeParams=["35","40"]
profile22 = part.CreateProfile(ProfileParam22,False)
part.BlankElement(profile22[0],True)
part.SetElementColor(profile22[0],"255","0","0","0.19999998807907104")
extrudeParam17 = part.CreateLinearSweepParam()
extrudeParam17.Name="積-押し出し22"
extrudeParam17.AddProfile(extrude_sheet2)
extrudeParam17.DirectionType="N"
extrudeParam17.DirectionParameter1="50000"
extrudeParam17.SweepDirection="+Z"
extrudeParam17.RefByGeometricMethod=False
extrude11 = part.CreateLinearSweep(solid1,"*",extrudeParam17,False)
solid4 = part.CreateSolid("HK.Casing.Deck.D","","SS400")
part.BlankElement(solid4,True)
part.SetElementColor(solid4,"139","69","19","0.78999996185302734")
thicken4 = part.CreateThicken("厚み付け3",solid4,"+",[extrude_sheet4],"+","10","0","0",False,False)
extrudeParam18 = part.CreateLinearSweepParam()
extrudeParam18.Name="積-押し出し3"
extrudeParam18.AddProfile(skt_pl4+",Edge00")
extrudeParam18.DirectionType="N"
extrudeParam18.DirectionParameter1="50000"
extrudeParam18.SweepDirection="+Z"
extrudeParam18.RefByGeometricMethod=False
extrude12 = part.CreateLinearSweep(solid4,"*",extrudeParam18,False)
extrudeParam19 = part.CreateLinearSweepParam()
extrudeParam19.Name="削除-押し出し1"
extrudeParam19.AddProfile(skt_pl4+",Edge01")
extrudeParam19.DirectionType="T"
extrudeParam19.RefByGeometricMethod=False
extrude13 = part.CreateLinearSweep(solid4,"-",extrudeParam19,False)
separated_bodies16 = part.BodyDivideByCurves("Separe body by curves1",solid4,[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies16[0],"139","69","19","0.78999996185302734")
part.SetElementColor(separated_bodies16[1],"139","69","19","0.78999996185302734")
separated_bodies17 = part.BodyDivideByCurves("Separe body by curves15",profile16[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies17[0],"148","0","211","0.39999997615814209")
part.SetElementColor(separated_bodies17[1],"148","0","211","0.39999997615814209")
separated_bodies18 = part.BodyDivideByCurves("Separe body by curves2",profile3[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies18[0],"255","0","0","0.19999998807907104")
var_elm14 = part.CreateVariable("FR7","4690","mm","")
ProfileParam23 = part.CreateProfileParam()
ProfileParam23.DefinitionType=1
ProfileParam23.BasePlane="PL,O,"+var_elm14+","+"X"
ProfileParam23.AddAttachSurfaces(extrude_sheet5)
ProfileParam23.ProfileName="HK.Casing.Wall.Side.FR07.CDP"
ProfileParam23.MaterialName="SS400"
ProfileParam23.ProfileType=1002
ProfileParam23.ProfileParams=["150","90","9.0000000000000018","12","6"]
ProfileParam23.Mold="+"
ProfileParam23.ReverseDir=False
ProfileParam23.ReverseAngle=True
ProfileParam23.CalcSnipOnlyAttachLines=False
ProfileParam23.AttachDirMethod=0
ProfileParam23.CCWDefAngle=False
ProfileParam23.AddEnd1Elements(extrude_sheet4)
ProfileParam23.End1Type=1102
ProfileParam23.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam23.AddEnd2Elements(extrude_sheet2)
ProfileParam23.End2Type=1102
ProfileParam23.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam23.End1ScallopType=1121
ProfileParam23.End1ScallopTypeParams=["35","40"]
ProfileParam23.End2ScallopType=1121
ProfileParam23.End2ScallopTypeParams=["35","40"]
profile23 = part.CreateProfile(ProfileParam23,False)
part.BlankElement(profile23[0],True)
part.SetElementColor(profile23[0],"255","0","0","0.19999998807907104")
ProfileParam24 = part.CreateProfileParam()
ProfileParam24.DefinitionType=1
ProfileParam24.BasePlane="PL,O,"+var_elm3+","+"Y"
ProfileParam24.AddAttachSurfaces(extrude_sheet3)
ProfileParam24.ProfileName="HK.Casing.Wall.Fore.DL05.CDP"
ProfileParam24.MaterialName="SS400"
ProfileParam24.ProfileType=1002
ProfileParam24.ProfileParams=["125","75","7","10","5"]
ProfileParam24.Mold="+"
ProfileParam24.ReverseDir=True
ProfileParam24.ReverseAngle=True
ProfileParam24.CalcSnipOnlyAttachLines=False
ProfileParam24.AttachDirMethod=0
ProfileParam24.CCWDefAngle=False
ProfileParam24.AddEnd1Elements(profile4[0])
ProfileParam24.End1Type=1102
ProfileParam24.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam24.AddEnd2Elements(extrude_sheet2)
ProfileParam24.End2Type=1102
ProfileParam24.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam24.End1ScallopType=1120
ProfileParam24.End1ScallopTypeParams=["50"]
ProfileParam24.End2ScallopType=1120
ProfileParam24.End2ScallopTypeParams=["50"]
profile24 = part.CreateProfile(ProfileParam24,False)
part.BlankElement(profile24[0],True)
part.SetElementColor(profile24[0],"255","0","0","0.19999998807907104")
separated_bodies19 = part.BodyDivideByCurves("Separe body by curves5",profile11[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies19[0],"148","0","211","0.39999997615814209")
part.SetElementColor(separated_bodies19[1],"148","0","211","0.39999997615814209")
ProfileParam25 = part.CreateProfileParam()
ProfileParam25.DefinitionType=1
ProfileParam25.BasePlane="PL,O,"+var_elm1+","+"Y"
ProfileParam25.AddAttachSurfaces(extrude_sheet3)
ProfileParam25.ProfileName="HK.Casing.Wall.Fore.DL02.CDP"
ProfileParam25.MaterialName="SS400"
ProfileParam25.FlangeName="HK.Casing.Wall.Fore.DL02.CDP"
ProfileParam25.FlangeMaterialName="SS400"
ProfileParam25.ProfileType=1201
ProfileParam25.ProfileParams=["150","12","388","10"]
ProfileParam25.Mold="-"
ProfileParam25.ReverseDir=True
ProfileParam25.ReverseAngle=False
ProfileParam25.CalcSnipOnlyAttachLines=False
ProfileParam25.AttachDirMethod=0
ProfileParam25.CCWDefAngle=False
ProfileParam25.AddEnd1Elements(profile1[1])
ProfileParam25.End1Type=1102
ProfileParam25.End1TypeParams=["25","14.999999999999998","0","0"]
ProfileParam25.AddEnd2Elements(extrude_sheet2)
ProfileParam25.End2Type=1102
ProfileParam25.End2TypeParams=["25","14.999999999999998","0","0"]
ProfileParam25.End1ScallopType=1120
ProfileParam25.End1ScallopTypeParams=["50"]
ProfileParam25.End2ScallopType=1120
ProfileParam25.End2ScallopTypeParams=["50"]
profile25 = part.CreateProfile(ProfileParam25,False)
part.BlankElement(profile25[0],True)
part.SetElementColor(profile25[0],"148","0","211","0.39999997615814209")
part.BlankElement(profile25[1],True)
part.SetElementColor(profile25[1],"148","0","211","0.39999997615814209")
ProfileParam26 = part.CreateProfileParam()
ProfileParam26.DefinitionType=1
ProfileParam26.BasePlane="PL,O,"+var_elm12+","+"Y"
ProfileParam26.AddAttachSurfaces(extrude_sheet1)
ProfileParam26.ProfileName="HK.Casing.Wall.Aft.DL03.CDP"
ProfileParam26.MaterialName="SS400"
ProfileParam26.ProfileType=1002
ProfileParam26.ProfileParams=["125","75","7","10","5"]
ProfileParam26.Mold="+"
ProfileParam26.ReverseDir=False
ProfileParam26.ReverseAngle=True
ProfileParam26.CalcSnipOnlyAttachLines=False
ProfileParam26.AttachDirMethod=0
ProfileParam26.CCWDefAngle=False
ProfileParam26.AddEnd1Elements(profile21[0])
ProfileParam26.End1Type=1102
ProfileParam26.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam26.AddEnd2Elements(extrude_sheet2)
ProfileParam26.End2Type=1102
ProfileParam26.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam26.End1ScallopType=1120
ProfileParam26.End1ScallopTypeParams=["50"]
ProfileParam26.End2ScallopType=1120
ProfileParam26.End2ScallopTypeParams=["50"]
profile26 = part.CreateProfile(ProfileParam26,False)
part.BlankElement(profile26[0],True)
part.SetElementColor(profile26[0],"255","0","0","0.19999998807907104")
separated_bodies20 = part.BodyDivideByCurves("Separe body by curves41",profile26[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies20[0],"255","0","0","0.19999998807907104")
ProfileParam27 = part.CreateProfileParam()
ProfileParam27.DefinitionType=1
ProfileParam27.BasePlane="PL,O,"+var_elm11+","+"X"
ProfileParam27.AddAttachSurfaces(extrude_sheet4)
ProfileParam27.ProfileName="HK.Casing.Deck.D.FR09P"
ProfileParam27.MaterialName="SS400"
ProfileParam27.ProfileType=1003
ProfileParam27.ProfileParams=["300","90","11","16","19","9.5"]
ProfileParam27.Mold="+"
ProfileParam27.ReverseDir=True
ProfileParam27.ReverseAngle=False
ProfileParam27.CalcSnipOnlyAttachLines=False
ProfileParam27.AttachDirMethod=0
ProfileParam27.CCWDefAngle=False
ProfileParam27.AddEnd1Elements(profile1[0])
ProfileParam27.End1Type=1102
ProfileParam27.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam27.AddEnd2Elements(extrude_sheet5)
ProfileParam27.End2Type=1102
ProfileParam27.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam27.End1ScallopType=1120
ProfileParam27.End1ScallopTypeParams=["50"]
ProfileParam27.End2ScallopType=1120
ProfileParam27.End2ScallopTypeParams=["50"]
profile27 = part.CreateProfile(ProfileParam27,False)
part.BlankElement(profile27[0],True)
part.SetElementColor(profile27[0],"148","0","211","0.39999997615814209")
separated_bodies21 = part.BodyDivideByCurves("Separe body by curves59",profile25[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies21[0],"148","0","211","0.39999997615814209")
ProfileParam28 = part.CreateProfileParam()
ProfileParam28.DefinitionType=1
ProfileParam28.BasePlane="PL,O,"+var_elm11+","+"X"
ProfileParam28.AddAttachSurfaces(extrude_sheet5)
ProfileParam28.ProfileName="HK.Casing.Wall.Side.FR09.CDP"
ProfileParam28.MaterialName="SS400"
ProfileParam28.ProfileType=1003
ProfileParam28.ProfileParams=["200","90","9.0000000000000018","14","14","7"]
ProfileParam28.Mold="+"
ProfileParam28.ReverseDir=False
ProfileParam28.ReverseAngle=True
ProfileParam28.CalcSnipOnlyAttachLines=False
ProfileParam28.AttachDirMethod=0
ProfileParam28.CCWDefAngle=False
ProfileParam28.AddEnd1Elements(profile27[0])
ProfileParam28.End1Type=1102
ProfileParam28.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam28.AddEnd2Elements(extrude_sheet2)
ProfileParam28.End2Type=1103
ProfileParam28.End2TypeParams=["0"]
ProfileParam28.End1ScallopType=1120
ProfileParam28.End1ScallopTypeParams=["50"]
ProfileParam28.End2ScallopType=1120
ProfileParam28.End2ScallopTypeParams=["50"]
profile28 = part.CreateProfile(ProfileParam28,False)
part.BlankElement(profile28[0],True)
part.SetElementColor(profile28[0],"148","0","211","0.39999997615814209")
ProfileParam29 = part.CreateProfileParam()
ProfileParam29.DefinitionType=1
ProfileParam29.BasePlane="PL,O,"+var_elm12+","+"Y"
ProfileParam29.AddAttachSurfaces(extrude_sheet3)
ProfileParam29.ProfileName="HK.Casing.Wall.Fore.DL03.CDP"
ProfileParam29.MaterialName="SS400"
ProfileParam29.ProfileType=1002
ProfileParam29.ProfileParams=["125","75","7","10","5"]
ProfileParam29.Mold="+"
ProfileParam29.ReverseDir=True
ProfileParam29.ReverseAngle=True
ProfileParam29.CalcSnipOnlyAttachLines=False
ProfileParam29.AttachDirMethod=0
ProfileParam29.CCWDefAngle=False
ProfileParam29.AddEnd1Elements(profile21[0])
ProfileParam29.End1Type=1102
ProfileParam29.End1TypeParams=["25","29.999999999999996","0","0"]
ProfileParam29.AddEnd2Elements(extrude_sheet2)
ProfileParam29.End2Type=1102
ProfileParam29.End2TypeParams=["25","29.999999999999996","0","0"]
ProfileParam29.End1ScallopType=1120
ProfileParam29.End1ScallopTypeParams=["50"]
ProfileParam29.End2ScallopType=1120
ProfileParam29.End2ScallopTypeParams=["50"]
profile29 = part.CreateProfile(ProfileParam29,False)
part.BlankElement(profile29[0],True)
part.SetElementColor(profile29[0],"255","0","0","0.19999998807907104")
separated_bodies22 = part.BodyDivideByCurves("Separe body by curves31",profile29[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies22[0],"255","0","0","0.19999998807907104")
separated_bodies23 = part.BodyDivideByCurves("Separe body by curves28",solid2,[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies23[0],"139","69","19","0.79999995231628418")
part.SetElementColor(separated_bodies23[1],"139","69","19","0.79999995231628418")
separated_bodies24 = part.BodyDivideByCurves("Separe body by curves53",profile1[1],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies24[0],"148","0","211","0.39999997615814209")
separated_bodies25 = part.BodyDivideByCurves("Separe body by curves12",profile27[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies25[0],"148","0","211","0.39999997615814209")
separated_bodies26 = part.BodyDivideByCurves("Separe body by curves26",profile17[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies26[0],"255","0","0","0.19999998807907104")
separated_bodies27 = part.BodyDivideByCurves("Separe body by curves25",profile23[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies27[0],"255","0","0","0.19999998807907104")
separated_bodies28 = part.BodyDivideByCurves("Separe body by curves57",profile25[1],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies28[0],"148","0","211","0.39999997615814209")
separated_bodies29 = part.BodyDivideByCurves("Separe body by curves58",profile2[1],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies29[0],"148","0","211","0.38999998569488525")
separated_bodies30 = part.BodyDivideByCurves("Separe body by curves24",profile22[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies30[0],"255","0","0","0.19999998807907104")
separated_bodies31 = part.BodyDivideByCurves("Separe body by curves4",solid1,[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies31[0],"139","69","19","0.79999995231628418")
part.SetElementColor(separated_bodies31[1],"139","69","19","0.79999995231628418")
separated_bodies32 = part.BodyDivideByCurves("Separe body by curves9",profile6[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies32[0],"255","0","0","0.19999998807907104")
separated_bodies33 = part.BodyDivideByCurves("Separe body by curves22",profile7[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies33[0],"255","0","0","0.19999998807907104")
separated_bodies34 = part.BodyDivideByCurves("Separe body by curves51",profile28[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies34[0],"148","0","211","0.39999997615814209")
separated_bodies35 = part.BodyDivideByCurves("Separe body by curves34",profile8[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies35[0],"255","0","0","0.19999998807907104")
separated_bodies36 = part.BodyDivideByCurves("Separe body by curves30",profile24[0],[skt_pl1],False,"0","","",False)
part.SetElementColor(separated_bodies36[0],"255","0","0","0.19999998807907104")



bracketParam1 = part.CreateBracketParam()
print(dir(bracketParam1))
help(bracketParam1)
help(part.CreateBracket)
bracketParam1.DefinitionType=1
bracketParam1.BracketName="ソリッド81"
bracketParam1.MaterialName="SS400"
bracketParam1.BaseElement=separated_bodies6[0]
bracketParam1.UseSideSheetForPlane=False
bracketParam1.Mold="B"
bracketParam1.Thickness="2"
bracketParam1.MoldOffset="-12.000000000000004"
bracketParam1.BracketType=1503
bracketParam1.BracketParams=["500","300"]
bracketParam1.Scallop1Type=1801
bracketParam1.Scallop1Params=["0"]
bracketParam1.Scallop2Type=0
bracketParam1.Surfaces1=[separated_bodies24[0]+",F,7695,1595.0000000000002,26386.000000000004"]
bracketParam1.RevSf1=False
bracketParam1.Surfaces2=["PLS","True","False","-1","-0","0",separated_bodies28[0]]
bracketParam1.RevSf2=False
bracketParam1.RevSf3=False
bracketParam1.Sf1DimensionType=1531
bracketParam1.Sf1DimensonParams=["600","15"]
bracketParam1.Sf2DimensionType=1531
bracketParam1.Sf2DimensonParams=["600","15"]
bracket1 = part.CreateBracket(bracketParam1,False)
part.SetElementColor(bracket1,"225","225","225","0")

# ブラケットセクション（bracketPram1 から始まり、最後のSetElementColorで終わる）

# ブラケットセクション（bracketPram1 から始まり、最後のSetElementColorで終わる）

bracketPram1 = part.CreateBracketParam()
bracketPram1.DefinitionType=1
bracketPram1.BracketName="HK.Wall.Aft.DL02.Deck.D"
bracketPram1.MaterialName="SS400"
bracketPram1.BaseElement=separated_bodies11[0]
bracketPram1.UseSideSheetForPlane=False
bracketPram1.Mold="-"
bracketPram1.Thickness="12"
bracketPram1.BracketType=1505
bracketPram1.BracketParams=["200"]
bracketPram1.Scallop1Type=1801
bracketPram1.Scallop1Params=["0"]
bracketPram1.Scallop2Type=0
bracketPram1.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram1.RevSf1=False
bracketPram1.Surfaces2=[separated_bodies11[0]+",FL"]
bracketPram1.RevSf2=False
bracketPram1.RevSf3=False
bracketPram1.Sf1DimensionType=1541
bracketPram1.Sf1DimensonParams=["0","100"]
bracketPram1.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies24[0]]
bracketPram1.Sf2DimensionType=1531
bracketPram1.Sf2DimensonParams=["200","15"]
bracket1 = part.CreateBracket(bracketPram1,False)
part.SetElementColor(bracket1,"0","255","255","0.19999998807907104")

bracketPram2 = part.CreateBracketParam()
bracketPram2.DefinitionType=1
bracketPram2.BracketName="HK.Wall.Fore.DL02.Deck.D"
bracketPram2.MaterialName="SS400"
bracketPram2.BaseElement=separated_bodies21[0]
bracketPram2.UseSideSheetForPlane=False
bracketPram2.Mold="-"
bracketPram2.Thickness="12"
bracketPram2.BracketType=1505
bracketPram2.BracketParams=["200"]
bracketPram2.Scallop1Type=1801
bracketPram2.Scallop1Params=["0"]
bracketPram2.Scallop2Type=0
bracketPram2.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram2.RevSf1=False
bracketPram2.Surfaces2=[separated_bodies21[0]+",FL"]
bracketPram2.RevSf2=False
bracketPram2.RevSf3=False
bracketPram2.Sf1DimensionType=1541
bracketPram2.Sf1DimensonParams=["0","100"]
bracketPram2.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies24[0]]
bracketPram2.Sf2DimensionType=1531
bracketPram2.Sf2DimensonParams=["200","15"]
bracket2 = part.CreateBracket(bracketPram2,False)
part.SetElementColor(bracket2,"0","255","255","0.19999998807907104")

bracketPram3 = part.CreateBracketParam()
bracketPram3.DefinitionType=1
bracketPram3.BracketName="HK.Wall.Side.FR13.Deck.D"
bracketPram3.MaterialName="SS400"
bracketPram3.BaseElement=separated_bodies13[0]
bracketPram3.UseSideSheetForPlane=False
bracketPram3.Mold="+"
bracketPram3.Thickness="9.0000000000000018"
bracketPram3.BracketType=1505
bracketPram3.BracketParams=["200"]
bracketPram3.Scallop1Type=1801
bracketPram3.Scallop1Params=["0"]
bracketPram3.Scallop2Type=0
bracketPram3.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram3.RevSf1=False
bracketPram3.Surfaces2=[separated_bodies13[0]+",FL"]
bracketPram3.RevSf2=False
bracketPram3.RevSf3=False
bracketPram3.Sf1DimensionType=1541
bracketPram3.Sf1DimensonParams=["0","100"]
bracketPram3.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies2[0]]
bracketPram3.Sf2DimensionType=1531
bracketPram3.Sf2DimensonParams=["200","15"]
bracket3 = part.CreateBracket(bracketPram3,False)
part.SetElementColor(bracket3,"0","255","255","0.19999998807907104")

bracketPram4 = part.CreateBracketParam()
bracketPram4.DefinitionType=1
bracketPram4.BracketName="HK.Wall.Aft.DL04.Deck.D"
bracketPram4.MaterialName="SS400"
bracketPram4.BaseElement=separated_bodies35[0]
bracketPram4.UseSideSheetForPlane=False
bracketPram4.Mold="+"
bracketPram4.Thickness="7"
bracketPram4.BracketType=1505
bracketPram4.BracketParams=["200"]
bracketPram4.Scallop1Type=1801
bracketPram4.Scallop1Params=["0"]
bracketPram4.Scallop2Type=0
bracketPram4.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram4.RevSf1=False
bracketPram4.Surfaces2=[separated_bodies35[0]+",FL"]
bracketPram4.RevSf2=False
bracketPram4.RevSf3=False
bracketPram4.Sf1DimensionType=1541
bracketPram4.Sf1DimensonParams=["0","100"]
bracketPram4.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies33[0]]
bracketPram4.Sf2DimensionType=1531
bracketPram4.Sf2DimensonParams=["200","15"]
bracket4 = part.CreateBracket(bracketPram4,False)
part.SetElementColor(bracket4,"0","255","255","0.19999998807907104")

bracketPram5 = part.CreateBracketParam()
bracketPram5.DefinitionType=1
bracketPram5.BracketName="HK.Wall.Fore.DL04.Deck.D"
bracketPram5.MaterialName="SS400"
bracketPram5.BaseElement=separated_bodies12[0]
bracketPram5.UseSideSheetForPlane=False
bracketPram5.Mold="+"
bracketPram5.Thickness="7"
bracketPram5.BracketType=1505
bracketPram5.BracketParams=["200"]
bracketPram5.Scallop1Type=1801
bracketPram5.Scallop1Params=["0"]
bracketPram5.Scallop2Type=0
bracketPram5.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram5.RevSf1=False
bracketPram5.Surfaces2=[separated_bodies12[0]+",FL"]
bracketPram5.RevSf2=False
bracketPram5.RevSf3=False
bracketPram5.Sf1DimensionType=1541
bracketPram5.Sf1DimensonParams=["0","100"]
bracketPram5.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies33[0]]
bracketPram5.Sf2DimensionType=1531
bracketPram5.Sf2DimensonParams=["200","15"]
bracket5 = part.CreateBracket(bracketPram5,False)
part.SetElementColor(bracket5,"0","255","255","0.19999998807907104")

bracketPram6 = part.CreateBracketParam()
bracketPram6.DefinitionType=1
bracketPram6.BracketName="HK.Wall.Aft.DL05.Deck.D"
bracketPram6.MaterialName="SS400"
bracketPram6.BaseElement=separated_bodies3[0]
bracketPram6.UseSideSheetForPlane=False
bracketPram6.Mold="+"
bracketPram6.Thickness="7"
bracketPram6.BracketType=1505
bracketPram6.BracketParams=["200"]
bracketPram6.Scallop1Type=1801
bracketPram6.Scallop1Params=["0"]
bracketPram6.Scallop2Type=0
bracketPram6.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram6.RevSf1=False
bracketPram6.Surfaces2=[separated_bodies3[0]+",FL"]
bracketPram6.RevSf2=False
bracketPram6.RevSf3=False
bracketPram6.Sf1DimensionType=1541
bracketPram6.Sf1DimensonParams=["0","100"]
bracketPram6.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies15[0]]
bracketPram6.Sf2DimensionType=1531
bracketPram6.Sf2DimensonParams=["200","15"]
bracket6 = part.CreateBracket(bracketPram6,False)
part.SetElementColor(bracket6,"0","255","255","0.19999998807907104")

bracketPram7 = part.CreateBracketParam()
bracketPram7.DefinitionType=1
bracketPram7.BracketName="HK.Wall.Fore.DL05.Deck.D"
bracketPram7.MaterialName="SS400"
bracketPram7.BaseElement=separated_bodies36[0]
bracketPram7.UseSideSheetForPlane=False
bracketPram7.Mold="+"
bracketPram7.Thickness="7"
bracketPram7.BracketType=1505
bracketPram7.BracketParams=["200"]
bracketPram7.Scallop1Type=1801
bracketPram7.Scallop1Params=["0"]
bracketPram7.Scallop2Type=0
bracketPram7.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram7.RevSf1=False
bracketPram7.Surfaces2=[separated_bodies36[0]+",FL"]
bracketPram7.RevSf2=False
bracketPram7.RevSf3=False
bracketPram7.Sf1DimensionType=1541
bracketPram7.Sf1DimensonParams=["0","100"]
bracketPram7.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies15[0]]
bracketPram7.Sf2DimensionType=1531
bracketPram7.Sf2DimensonParams=["200","15"]
bracket7 = part.CreateBracket(bracketPram7,False)
part.SetElementColor(bracket7,"0","255","255","0.19999998807907104")

bracketPram8 = part.CreateBracketParam()
bracketPram8.DefinitionType=1
bracketPram8.BracketName="HK.Wall.Aft.DL01.Deck.D"
bracketPram8.MaterialName="SS400"
bracketPram8.BaseElement=separated_bodies10[0]
bracketPram8.UseSideSheetForPlane=False
bracketPram8.Mold="+"
bracketPram8.Thickness="7"
bracketPram8.BracketType=1505
bracketPram8.BracketParams=["200"]
bracketPram8.Scallop1Type=1801
bracketPram8.Scallop1Params=["0"]
bracketPram8.Scallop2Type=0
bracketPram8.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram8.RevSf1=False
bracketPram8.Surfaces2=[separated_bodies10[0]+",FL"]
bracketPram8.RevSf2=False
bracketPram8.RevSf3=False
bracketPram8.Sf1DimensionType=1541
bracketPram8.Sf1DimensonParams=["0","100"]
bracketPram8.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies26[0]]
bracketPram8.Sf2DimensionType=1531
bracketPram8.Sf2DimensonParams=["200","15"]
bracket8 = part.CreateBracket(bracketPram8,False)
part.SetElementColor(bracket8,"0","255","255","0.19999998807907104")

bracketPram9 = part.CreateBracketParam()
bracketPram9.DefinitionType=1
bracketPram9.BracketName="HK.Wall.Fore.DL01.Deck.D"
bracketPram9.MaterialName="SS400"
bracketPram9.BaseElement=separated_bodies9[0]
bracketPram9.UseSideSheetForPlane=False
bracketPram9.Mold="+"
bracketPram9.Thickness="7"
bracketPram9.BracketType=1505
bracketPram9.BracketParams=["200"]
bracketPram9.Scallop1Type=1801
bracketPram9.Scallop1Params=["0"]
bracketPram9.Scallop2Type=0
bracketPram9.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram9.RevSf1=False
bracketPram9.Surfaces2=[separated_bodies9[0]+",FL"]
bracketPram9.RevSf2=False
bracketPram9.RevSf3=False
bracketPram9.Sf1DimensionType=1541
bracketPram9.Sf1DimensonParams=["0","100"]
bracketPram9.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies4[0]]
bracketPram9.Sf2DimensionType=1531
bracketPram9.Sf2DimensonParams=["200","15"]
bracket9 = part.CreateBracket(bracketPram9,False)
part.SetElementColor(bracket9,"0","255","255","0.19999998807907104")

bracketPram10 = part.CreateBracketParam()
bracketPram10.DefinitionType=1
bracketPram10.BracketName="HK.Wall.Aft.DL03.Deck.D"
bracketPram10.MaterialName="SS400"
bracketPram10.BaseElement=separated_bodies20[0]
bracketPram10.UseSideSheetForPlane=False
bracketPram10.Mold="+"
bracketPram10.Thickness="7"
bracketPram10.BracketType=1505
bracketPram10.BracketParams=["200"]
bracketPram10.Scallop1Type=1801
bracketPram10.Scallop1Params=["0"]
bracketPram10.Scallop2Type=0
bracketPram10.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram10.RevSf1=False
bracketPram10.Surfaces2=[separated_bodies20[0]+",FL"]
bracketPram10.RevSf2=False
bracketPram10.RevSf3=False
bracketPram10.Sf1DimensionType=1541
bracketPram10.Sf1DimensonParams=["0","100"]
bracketPram10.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies14[0]]
bracketPram10.Sf2DimensionType=1531
bracketPram10.Sf2DimensonParams=["200","15"]
bracket10 = part.CreateBracket(bracketPram10,False)
part.SetElementColor(bracket10,"0","255","255","0.19999998807907104")

bracketPram11 = part.CreateBracketParam()
bracketPram11.DefinitionType=1
bracketPram11.BracketName="HK.Wall.Fore.DL03.Deck.D"
bracketPram11.MaterialName="SS400"
bracketPram11.BaseElement=separated_bodies22[0]
bracketPram11.UseSideSheetForPlane=False
bracketPram11.Mold="+"
bracketPram11.Thickness="7"
bracketPram11.BracketType=1505
bracketPram11.BracketParams=["200"]
bracketPram11.Scallop1Type=1801
bracketPram11.Scallop1Params=["0"]
bracketPram11.Scallop2Type=0
bracketPram11.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram11.RevSf1=False
bracketPram11.Surfaces2=[separated_bodies22[0]+",FL"]
bracketPram11.RevSf2=False
bracketPram11.RevSf3=False
bracketPram11.Sf1DimensionType=1541
bracketPram11.Sf1DimensonParams=["0","100"]
bracketPram11.Sf1EndElements=["PLS","False","False","0","-1","0",separated_bodies14[0]]
bracketPram11.Sf2DimensionType=1531
bracketPram11.Sf2DimensonParams=["200","15"]
bracket11 = part.CreateBracket(bracketPram11,False)
part.SetElementColor(bracket11,"0","255","255","0.19999998807907104")

bracketPram12 = part.CreateBracketParam()
bracketPram12.DefinitionType=1
bracketPram12.BracketName="HK.Wall.Side.FR09.Deck.D"
bracketPram12.MaterialName="SS400"
bracketPram12.BaseElement=separated_bodies34[0]
bracketPram12.UseSideSheetForPlane=False
bracketPram12.Mold="+"
bracketPram12.Thickness="9.0000000000000018"
bracketPram12.BracketType=1505
bracketPram12.BracketParams=["200"]
bracketPram12.Scallop1Type=1801
bracketPram12.Scallop1Params=["0"]
bracketPram12.Scallop2Type=0
bracketPram12.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram12.RevSf1=False
bracketPram12.Surfaces2=[separated_bodies34[0]+",FL"]
bracketPram12.RevSf2=False
bracketPram12.RevSf3=False
bracketPram12.Sf1DimensionType=1541
bracketPram12.Sf1DimensonParams=["0","100"]
bracketPram12.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies25[0]]
bracketPram12.Sf2DimensionType=1531
bracketPram12.Sf2DimensonParams=["200","15"]
bracket12 = part.CreateBracket(bracketPram12,False)
part.SetElementColor(bracket12,"0","255","255","0.19999998807907104")

bracketPram13 = part.CreateBracketParam()
bracketPram13.DefinitionType=1
bracketPram13.BracketName="HK.Wall.Side.FR12.Deck.D"
bracketPram13.MaterialName="SS400"
bracketPram13.BaseElement=separated_bodies18[0]
bracketPram13.UseSideSheetForPlane=False
bracketPram13.Mold="+"
bracketPram13.Thickness="9.0000000000000018"
bracketPram13.BracketType=1505
bracketPram13.BracketParams=["200"]
bracketPram13.Scallop1Type=1801
bracketPram13.Scallop1Params=["0"]
bracketPram13.Scallop2Type=0
bracketPram13.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram13.RevSf1=False
bracketPram13.Surfaces2=[separated_bodies18[0]+",FL"]
bracketPram13.RevSf2=False
bracketPram13.RevSf3=False
bracketPram13.Sf1DimensionType=1541
bracketPram13.Sf1DimensonParams=["0","100"]
bracketPram13.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies2[0]]
bracketPram13.Sf2DimensionType=1531
bracketPram13.Sf2DimensonParams=["200","15"]
bracket13 = part.CreateBracket(bracketPram13,False)
part.SetElementColor(bracket13,"0","255","255","0.19999998807907104")

bracketPram14 = part.CreateBracketParam()
bracketPram14.DefinitionType=1
bracketPram14.BracketName="HK.Wall.Side.FR11.Deck.D"
bracketPram14.MaterialName="SS400"
bracketPram14.BaseElement=separated_bodies1[0]
bracketPram14.UseSideSheetForPlane=False
bracketPram14.Mold="+"
bracketPram14.Thickness="9.0000000000000018"
bracketPram14.BracketType=1505
bracketPram14.BracketParams=["200"]
bracketPram14.Scallop1Type=1801
bracketPram14.Scallop1Params=["0"]
bracketPram14.Scallop2Type=0
bracketPram14.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram14.RevSf1=False
bracketPram14.Surfaces2=[separated_bodies1[0]+",FL"]
bracketPram14.RevSf2=False
bracketPram14.RevSf3=False
bracketPram14.Sf1DimensionType=1541
bracketPram14.Sf1DimensonParams=["0","100"]
bracketPram14.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies2[0]]
bracketPram14.Sf2DimensionType=1531
bracketPram14.Sf2DimensonParams=["200","15"]
bracket14 = part.CreateBracket(bracketPram14,False)
part.SetElementColor(bracket14,"0","255","255","0.19999998807907104")

bracketPram15 = part.CreateBracketParam()
bracketPram15.DefinitionType=1
bracketPram15.BracketName="HK.Wall.Side.FR15.Deck.D"
bracketPram15.MaterialName="SS400"
bracketPram15.BaseElement=separated_bodies32[0]
bracketPram15.UseSideSheetForPlane=False
bracketPram15.Mold="+"
bracketPram15.Thickness="9.0000000000000018"
bracketPram15.BracketType=1505
bracketPram15.BracketParams=["200"]
bracketPram15.Scallop1Type=1801
bracketPram15.Scallop1Params=["0"]
bracketPram15.Scallop2Type=0
bracketPram15.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram15.RevSf1=False
bracketPram15.Surfaces2=[separated_bodies32[0]+",FL"]
bracketPram15.RevSf2=False
bracketPram15.RevSf3=False
bracketPram15.Sf1DimensionType=1541
bracketPram15.Sf1DimensonParams=["0","100"]
bracketPram15.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies2[0]]
bracketPram15.Sf2DimensionType=1531
bracketPram15.Sf2DimensonParams=["200","15"]
bracket15 = part.CreateBracket(bracketPram15,False)
part.SetElementColor(bracket15,"0","255","255","0.19999998807907104")

bracketPram16 = part.CreateBracketParam()
bracketPram16.DefinitionType=1
bracketPram16.BracketName="HK.Wall.Side.FR10.Deck.D"
bracketPram16.MaterialName="SS400"
bracketPram16.BaseElement=separated_bodies7[0]
bracketPram16.UseSideSheetForPlane=False
bracketPram16.Mold="+"
bracketPram16.Thickness="9.0000000000000018"
bracketPram16.BracketType=1505
bracketPram16.BracketParams=["200"]
bracketPram16.Scallop1Type=1801
bracketPram16.Scallop1Params=["0"]
bracketPram16.Scallop2Type=0
bracketPram16.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram16.RevSf1=False
bracketPram16.Surfaces2=[separated_bodies7[0]+",FL"]
bracketPram16.RevSf2=False
bracketPram16.RevSf3=False
bracketPram16.Sf1DimensionType=1541
bracketPram16.Sf1DimensonParams=["0","100"]
bracketPram16.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies25[0]]
bracketPram16.Sf2DimensionType=1531
bracketPram16.Sf2DimensonParams=["200","15"]
bracket16 = part.CreateBracket(bracketPram16,False)
part.SetElementColor(bracket16,"0","255","255","0.19999998807907104")

bracketPram17 = part.CreateBracketParam()
bracketPram17.DefinitionType=1
bracketPram17.BracketName="HK.Wall.Side.FR08.Deck.D"
bracketPram17.MaterialName="SS400"
bracketPram17.BaseElement=separated_bodies8[0]
bracketPram17.UseSideSheetForPlane=False
bracketPram17.Mold="+"
bracketPram17.Thickness="9.0000000000000018"
bracketPram17.BracketType=1505
bracketPram17.BracketParams=["200"]
bracketPram17.Scallop1Type=1801
bracketPram17.Scallop1Params=["0"]
bracketPram17.Scallop2Type=0
bracketPram17.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram17.RevSf1=False
bracketPram17.Surfaces2=[separated_bodies8[0]+",FL"]
bracketPram17.RevSf2=False
bracketPram17.RevSf3=False
bracketPram17.Sf1DimensionType=1541
bracketPram17.Sf1DimensonParams=["0","100"]
bracketPram17.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies25[0]]
bracketPram17.Sf2DimensionType=1531
bracketPram17.Sf2DimensonParams=["200","15"]
bracket17 = part.CreateBracket(bracketPram17,False)
part.SetElementColor(bracket17,"0","255","255","0.19999998807907104")

bracketPram18 = part.CreateBracketParam()
bracketPram18.DefinitionType=1
bracketPram18.BracketName="HK.Wall.Side.FR14.Deck.D"
bracketPram18.MaterialName="SS400"
bracketPram18.BaseElement=separated_bodies30[0]
bracketPram18.UseSideSheetForPlane=False
bracketPram18.Mold="+"
bracketPram18.Thickness="9.0000000000000018"
bracketPram18.BracketType=1505
bracketPram18.BracketParams=["200"]
bracketPram18.Scallop1Type=1801
bracketPram18.Scallop1Params=["0"]
bracketPram18.Scallop2Type=0
bracketPram18.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram18.RevSf1=False
bracketPram18.Surfaces2=[separated_bodies30[0]+",FL"]
bracketPram18.RevSf2=False
bracketPram18.RevSf3=False
bracketPram18.Sf1DimensionType=1541
bracketPram18.Sf1DimensonParams=["0","100"]
bracketPram18.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies2[0]]
bracketPram18.Sf2DimensionType=1531
bracketPram18.Sf2DimensonParams=["200","15"]
bracket18 = part.CreateBracket(bracketPram18,False)
part.SetElementColor(bracket18,"0","255","255","0.19999998807907104")

bracketPram19 = part.CreateBracketParam()
bracketPram19.DefinitionType=1
bracketPram19.BracketName="HK.Wall.Side.FR07.Deck.D"
bracketPram19.MaterialName="SS400"
bracketPram19.BaseElement=separated_bodies27[0]
bracketPram19.UseSideSheetForPlane=False
bracketPram19.Mold="+"
bracketPram19.Thickness="9.0000000000000018"
bracketPram19.BracketType=1505
bracketPram19.BracketParams=["200"]
bracketPram19.Scallop1Type=1801
bracketPram19.Scallop1Params=["0"]
bracketPram19.Scallop2Type=0
bracketPram19.Surfaces1=["PLS","False","False","0","0","-1",extrude_sheet4]
bracketPram19.RevSf1=False
bracketPram19.Surfaces2=[separated_bodies27[0]+",FL"]
bracketPram19.RevSf2=False
bracketPram19.RevSf3=False
bracketPram19.Sf1DimensionType=1541
bracketPram19.Sf1DimensonParams=["0","100"]
bracketPram19.Sf1EndElements=["PLS","False","False","-1","0","0",separated_bodies25[0]]
bracketPram19.Sf2DimensionType=1531
bracketPram19.Sf2DimensonParams=["200","15"]
bracket19 = part.CreateBracket(bracketPram19,False)
part.SetElementColor(bracket19,"0","255","255","0.19999998807907104")
