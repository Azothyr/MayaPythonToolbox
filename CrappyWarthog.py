import maya.cmds as cmds

cmds.polyCylinder(ax= [0, 0, 10], n= "body", r= 1, h= 5, sx= 9, sy= 10 ,sz= 1, rcp= 0, cuv= 3, ch= 1)
cmds.setAttr("body.rotateZ", 10)
cmds.setAttr("body.translateY", 3)

cmds.select('body.e[2]', r= True)
cmds.select('body.e[0:8]', add= True)
cmds.scale(0.0808783, 0.0808783, 0.0808783, p= [-3.84978e-08, 3.030154, -2.5], r=True)

cmds.select('body.e[10]', r= True)
cmds.select('body.e[9:17]', add= True)
cmds.scale(0.673725, 0.673725, 0.673725, p= [-3.84978e-08, 3.030154, -2], r=True)

cmds.select('body.e[20]', r= True)
cmds.select('body.e[18:26]', add= True)
cmds.scale(1.047865, 1.047865, 1.047865, p= [-3.84978e-08, 3.030154, -1.5], r= True)

cmds.select('body.e[29]', r= True)
cmds.select('body.e[27:35]', add= True)
cmds.scale(1.217996, 1.217996, 1.217996, p= [-3.84978e-08, 3.030154, -1], r= True)

cmds.select('body.e[38]', r= True)
cmds.select('body.e[36:44]', add= True)
cmds.scale(1.299037, 1.299037, 1.299037, p= [-3.84978e-08, 3.030154, -0.5], r= True)

cmds.select('body.e[47]', r= True)
cmds.select('body.e[45:53]', add= True)
cmds.scale(1.362088, 1.362088, 1.362088, p= [-3.84978e-08, 3.030154, 0], r= True)

cmds.select('body.e[56]', r= True)
cmds.select('body.e[54:62]', add= True)
cmds.scale(1.406457, 1.406457, 1.406457, p= [-3.84978e-08, 3.030154, 0.5], r= True)

cmds.select('body.e[65]', r= True)
cmds.select('body.e[63:71]', add= True)
cmds.scale(1.522814, 1.522814, 1.522814, p= [-3.84978e-08, 3.030154, 1], r= True)

cmds.select('body.e[74]', r= True)
cmds.select('body.e[72:80]', add= True)
cmds.scale(1.364495, 1.364495, 1.364495, p= [-3.84978e-08, 3.030154, 1.5], r= True)

cmds.select('body.e[92]', r= True)
cmds.select('body.e[90:98]', add= True)
cmds.scale(0.847765, 0.847765, 0.847765, p= [-3.84978e-08, 3.030154, 2.5], r= True)

cmds.select('body.vtx[95:96]', r= True)
cmds.move(0, 0, -0.233618, r= True)
cmds.select('body.vtx[94]', 'body.vtx[97]', r= True)
cmds.move(0, 0, -0.146519, r= True)
cmds.select('body.vtx[93]', 'body.vtx[98]', 'body.vtx[100]', r= True)
cmds.move(0, 0, -0.176026, r= True)
cmds.select('body.vtx[94]', 'body.vtx[97]', r= True)
cmds.move(0, 0, -0.120102, r= True)
cmds.select('body.vtx[95:96]', r= True)
cmds.move(0, 0, -0.0691537, r= True)
cmds.select('body.vtx[86:87]', r= True)
cmds.move(0, 0.0931111, 0, r= True)
cmds.select('body.vtx[90]', 'body.vtx[92]', r= True)
cmds.move(0, 0, -0.0841752, r= True)


cmds.polyCylinder(ax= [0, 0, 0], n= "leg", r= .35, h= 2, sx= 5, sy= 4, sz= 1, rcp= 0, cuv= 3, ch= 1)
cmds.setAttr('leg.rotateY', -15)
cmds.select('leg', r= True)
cmds.move(-1.2, 2, 1, r= True)
cmds.select('leg', r= True)
cmds.select('leg.vtx[22]', r= True)
cmds.move(0.114525, 0, 0, r= True)
cmds.select('leg.vtx[21]', r= True)
cmds.move(0.045446, 0, 0, r= True)
cmds.select('leg', r= True)
cmds.polyMirrorFace('leg', cutMesh=1, axis=0, axisDirection=1, mergeMode=1, mergeThresholdType=0, mergeThreshold=0.001, mirrorAxis=2, mirrorPosition=0, smoothingAngle=30, flipUVs=0, ch=1)
cmds.setAttr( 'polyMirror1.cutMesh', 0)


cmds.select('leg', r= True)
cmds.polyMirrorFace('leg', cutMesh=1, axis=0, axisDirection=1, mergeMode=1, mergeThresholdType=0, mergeThreshold=0.001, mirrorAxis=2, mirrorPosition=0, smoothingAngle=30, flipUVs=0, ch=1)
cmds.setAttr("polyMirror2.cutMesh", 0)
cmds.setAttr("polyMirror2.axis", 2)
cmds.select('leg', r= True)


cmds.select('leg', r= True)
cmds.polySeparate('leg', ch= 1)
cmds.select('polySurface3', r= True)
cmds.select('polySurface4', tgl= True)
cmds.polyUnite('polySurface3', 'polySurface4', name= 'backLegs', ch= 1, mergeUVSets= 1, centerPivot= True)
cmds.select('polySurface1', r= True)
cmds.select('polySurface2', tgl= True)
cmds.polyUnite('polySurface1', 'polySurface2', name= 'frontLegs', ch= 1, mergeUVSets= 1, centerPivot= True )


cmds.select('polySurface3', r= True)
cmds.scale(0.700962, 1, 1, r= True)


cmds.polySphere(name= 'eye',r= 0.15, sx= 10, sy= 10, ax= [0, 1, 0], cuv= 2, ch= 1)
cmds.move(0.4, 4, 1.75, r= True)
cmds.setAttr('eye.rotateX', 40)
cmds.select('eye.e[140]', r= True)
cmds.select('eye.e[46]', add= True)
cmds.softSelect(softSelectEnabled= True, ssd= 0.148015, sud= 0.5)
cmds.softSelect(ssd= 0.216988, sud= 0.5)
cmds.move(0, 0, -0.0607241, r= True)
cmds.select('eye.e[41]', r= True)
cmds.move(0, 0, 0.0643634, r= True)
cmds.select('eye', r= True)
cmds.polyMirrorFace('eye', cutMesh= 1, axis= 0, axisDirection= 1, mergeMode= 1, mergeThresholdType= 0, mergeThreshold= 0.001, mirrorAxis= 2, mirrorPosition= 0, smoothingAngle= 30, flipUVs= 0, ch= 1)