import win32com.client

# EvoShipを起動して3Dドキュメントとパートを作成
evoship = win32com.client.DispatchEx("EvoShip.Application")
evoship.Visible = True
doc = evoship.Create3DDocument()
part = doc.GetPart()

# 10cm（＝100mm）を示す変数EDGEを作成
# 以降の長さ指定や座標の式で "EDGE" を参照します
edge_var_id = part.CreateVariable("EDGE", 10.0, "cm", "")

# スケッチ平面を作成（グローバルXY平面）
# PlaneDef: "PL,Z" = グローバルXY平面
sketch_plane = part.CreateSketchPlane("SKP_XY", "", "PL,Z")

# スケッチレイヤーを作成
sketch_layer = part.CreateSketchLayer("SKL_Square", "SKP_XY")

# 正方形プロファイル（1辺=EDGE）を作成
# 点(2D)は "X,Y" の文字列で指定（数値や変数を式で利用可能）
p0 = "0.0,0.0"
p1 = "EDGE,0.0"
p2 = "EDGE,EDGE"
p3 = "0.0,EDGE"

# 4本のスケッチ直線で閉じたプロファイルを作成
l1 = part.CreateSketchLine(p0, "L1", p1, "SKL_Square")
l2 = part.CreateSketchLine(p1, "L2", p2, "SKL_Square")
l3 = part.CreateSketchLine(p2, "L3", p3, "SKL_Square")
l4 = part.CreateSketchLine(p3, "L4", p0, "SKL_Square")

# 押し出し先となる空のソリッドを作成
solid = part.CreateSolid("CubeSolid")

# 押し出し（線形スイープ）パラメータオブジェクトを作成
param = part.CreateLinearSweepParam()

# Paramオブジェクトへの設定を複数の方法で試すヘルパ
# 環境により属性/インデクサ/Setterメソッドの実装が異なる場合があるため冗長に対応
def set_param(p, name, value):
    # 属性として設定
    try:
        setattr(p, name, value)
        return
    except Exception:
        pass
    # インデクサとして設定
    try:
        p[name] = value
        return
    except Exception:
        pass
    # 代表的なSetterメソッド名を試行
    for m in ("SetParameter", "SetParam", "Set"):
        try:
            getattr(p, m)(name, value)
            return
        except Exception:
            pass

# プロファイルにスケッチレイヤーを指定し、距離=EDGEで押し出し
# 方向未指定時はスケッチ法線（ここでは+Z）方向にスイープ
set_param(param, "NAME", "ExtrudeCube")
set_param(param, "ElementGroup", "")
set_param(param, "MaterialName", "")
set_param(param, "Profile", ["SKL_Square"])           # プロファイルはスケッチ（レイヤー）を指定
set_param(param, "ProfileOffset", "0.0")
set_param(param, "DirectionParameter1", "EDGE")        # 押し出し距離 = 10cm（変数EDGE）
set_param(param, "bRefByGeometricMethod", False)
set_param(param, "bIntervalSwep", False)

# ソリッドへ押し出し形状を付加（オペレーションタイプ=ADD）
# TargetSolidName: "CubeSolid", OperationType: "ADD"
feature = part.CreateLinearSweep("CubeSolid", "ADD", param)

print("立方体を作成しました（1辺 = 10 cm）。")