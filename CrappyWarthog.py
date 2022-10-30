import maya.cmds as cmds

cmds.polySphere()
print ("hello")
//move sphere
move -r -os -wd 0 3 0 ;
//move -radius - objectSpace -worldSpaceDistance 0 3.868887 0 ;
//create a cylinder
polyCylinder -r 1 -h 5 -sx 9 -sy 10 -sz 1 -ax 0 0 10 -rcp 0 -cuv 3 -ch 1;
//polyCylinder -radius 1 -height 5 -subdivisionsX 20 -subdivisionsY 10 -subdivisionsZ 1 -axis 90 10 0 -roundCap 0 -createUVs 3 -constructHistory 1;
setAttr "pCylinder1.rotateZ" 10;
setAttr "polyCylinder1.subdivisionsAxis" 9;
setAttr "polyCylinder1.subdivisionsHeight" 10;
setAttr "pCylinder1.translateY" 3;
select -r pCylinder1.e[2] ;
select -add pCylinder1.e[0:8] ;
scale -r -p -3.84978e-08cm 3.030154cm -2.5cm 0.0808783 0.0808783 0.0808783 ;
select -r pCylinder1.e[10] ;
select -add pCylinder1.e[9:17] ;
scale -r -p -3.84978e-08cm 3.030154cm -2cm 0.673725 0.673725 0.673725 ;
select -r pCylinder1.e[20] ;
select -add pCylinder1.e[18:26] ;
scale -r -p -3.84978e-08cm 3.030154cm -1.5cm 1.047865 1.047865 1.047865 ;
select -r pCylinder1.e[29] ;
select -add pCylinder1.e[27:35] ;
scale -r -p -3.84978e-08cm 3.030154cm -1cm 1.217996 1.217996 1.217996 ;
select -r pCylinder1.e[38] ;
select -add pCylinder1.e[36:44] ;
select -r pCylinder1.e[38] ;
select -add pCylinder1.e[36:44] ;
scale -r -p -3.84978e-08cm 3.030154cm -0.5cm 1.299037 1.299037 1.299037 ;
select -r pCylinder1.e[47] ;
select -add pCylinder1.e[45:53] ;
scale -r -p -3.84978e-08cm 3.030154cm 0cm 1.362088 1.362088 1.362088 ;
select -r pCylinder1.e[56] ;
select -add pCylinder1.e[54:62] ;
scale -r -p -3.84978e-08cm 3.030154cm 0.5cm 1.406457 1.406457 1.406457 ;
select -r pCylinder1.e[65] ;
select -add pCylinder1.e[63:71] ;
scale -r -p -3.84978e-08cm 3.030154cm 1cm 1.522814 1.522814 1.522814 ;
select -r pCylinder1.e[74] ;
select -add pCylinder1.e[72:80] ;
scale -r -p -3.84978e-08cm 3.030154cm 1.5cm 1.364495 1.364495 1.364495 ;
select -r pCylinder1.e[92] ;
select -add pCylinder1.e[90:98] ;
scale -r -p -3.84978e-08cm 3.030154cm 2.5cm 0.847765 0.847765 0.847765 ;
select -r pCylinder1.vtx[95:96] ;
move -r 0 0 -0.233618 ;
select -r pCylinder1.vtx[94] pCylinder1.vtx[97] ;
move -r 0 0 -0.146519 ;
select -r pCylinder1.vtx[93] pCylinder1.vtx[98] pCylinder1.vtx[100] ;
move -r 0 0 -0.176026 ;
select -r pCylinder1.vtx[94] pCylinder1.vtx[97] ;
move -r 0 0 -0.120102 ;
select -r pCylinder1.vtx[95:96] ;
move -r 0 0 -0.0691537 ;
select -r pCylinder1.vtx[86:87] ;
move -r 0 0.0931111 0 ;
select -r pCylinder1.vtx[90] pCylinder1.vtx[92] ;
move -r 0 0 -0.0841752 ;

//Cylinder2 (front legs)
polyCylinder -r .35 -h 2 -sx 5 -sy 4 -sz 1 -ax 0 0 0 -rcp 0 -cuv 3 -ch 1;
setAttr "pCylinder2.rotateY" -15;
select -r pCylinder2 ;
move -r -1.2 2 1;
select -r pCylinder2 ;
select -r pCylinder2.vtx[22] ;
move -r 0.114525 0 0 ;
select -r pCylinder2.vtx[21] ;
move -r 0.045446 0 0 ;
select -cl  ;
select -r pCylinder2 ;
polyMirrorFace  -cutMesh 1 -axis 0 -axisDirection 1 -mergeMode 1 -mergeThresholdType 0 -mergeThreshold 0.001 -mirrorAxis 2 -mirrorPosition 0 -smoothingAngle 30 -flipUVs 0 -ch 1 pCylinder2;
// Result: polyMirror1
setAttr "polyMirror1.cutMesh" 0;
select -cl  ;

//create back legs
select -r pCylinder2 ;
polyMirrorFace  -cutMesh 1 -axis 0 -axisDirection 1 -mergeMode 1 -mergeThresholdType 0 -mergeThreshold 0.001 -mirrorAxis 2 -mirrorPosition 0 -smoothingAngle 30 -flipUVs 0 -ch 1 pCylinder2;
// Result: polyMirror2
setAttr "polyMirror2.cutMesh" 0;
setAttr "polyMirror2.axis" 2;
select -r pCylinder2 ;

//Seperate all legs, combine front and then combine back
select -r pCylinder2 ;
 polySeparate -ch 1 pCylinderShape2;
// Result: polySurface1 polySurface2 polySurface3 polySurface4 polySeparate1
select -r polySurface3 ;
select -tgl polySurface4 ;
polyUnite -ch 1 -mergeUVSets 1 -centerPivot -name polySurface3 polySurface3 polySurface4;
// Result: |polySurface3 polyUnite1
select -r polySurface1 ;
select -tgl polySurface2 ;
polyUnite -ch 1 -mergeUVSets 1 -centerPivot -name polySurface1 polySurface1 polySurface2;
// Result: |polySurface1 polyUnite2

//shrink back legs
select -r |polySurface3 ;
scale -r 0.700962 1 1 ;

//add eyes
polySphere -r 0.15 -sx 10 -sy 10 -ax 0 1 0 -cuv 2 -ch 1;
move -r 0.4 4 1.75 ;
setAttr "pSphere1.rotateX" -40;
select -r pSphere1.e[140] ;
select -r pSphere1.e[46] ;
softSelect -softSelectEnabled true -ssd 0.148015 -sud 0.5 ;
softSelect -ssd 0.216988 -sud 0.5 ;
move -r 0 0 -0.0607241 ;
select -r pSphere1.e[41] ;
move -r 0 0 0.0643634 ;
select -cl  ;
select -r pSphere1 ;
polyMirrorFace  -cutMesh 1 -axis 0 -axisDirection 1 -mergeMode 1 -mergeThresholdType 0 -mergeThreshold 0.001 -mirrorAxis 2 -mirrorPosition 0 -smoothingAngle 30 -flipUVs 0 -ch 1 pSphere1;
// Result: polyMirror3