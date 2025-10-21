import LogicState
import Reconization

secondCnt = 3


def convert_seconds_to_minutes(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes):02d}:{int(remaining_seconds):02d}"


def getMaxConfResult(rec_res):
    ret_res = []
    truck = Reconization.RecResult(0, 0, 0, 0, "Truck", -1)
    bucket0 = Reconization.RecResult(0, 0, 0, 0, "bucket0", -1)
    bucket1 = Reconization.RecResult(0, 0, 0, 0, "bucket1", -1)
    for rec in rec_res:
        if rec.label[:5] == "Truck":
            if rec.conf > truck.conf:
                truck = rec
        elif rec.label[6] == "0":
            if rec.conf > bucket0.conf:
                bucket0 = rec
        elif rec.label[6] == "1":
            if rec.conf > bucket1.conf:
                bucket1 = rec
    if truck.conf > 0:
        ret_res.append(truck)
    if bucket0.conf > 0 and bucket1.conf > 0:
        if bucket0.conf > bucket1.conf:
            ret_res.append(bucket0)
        else:
            ret_res.append(bucket1)
    elif bucket0.conf > 0:
        ret_res.append(bucket0)
    elif bucket1.conf > 0:
        ret_res.append(bucket1)
    return ret_res


def get_close_to(rec1, rec2):
    dis1 = rec1[0].get_distance(rec1[1])
    dis2 = rec2[0].get_distance(rec2[1])
    if dis1 < dis2:
        return -1
    elif dis1 == dis2:
        return 0
    else:
        return 1


def get_dou_state(rec_res):
    if len(rec_res) == 0:
        return -1
    a = rec_res[0].get_bucket_state()
    if a >= 0:
        return a
    if len(rec_res) == 1:
        return -1
    return rec_res[1].get_bucket_state()


def get_douY(rec_res):
    if len(rec_res) == 0:
        return -1
    if rec_res[0].label[:5] != "truck":
        return rec_res[0].y
    if len(rec_res) == 2:
        return rec_res[1].y
    return -1


def TransState1(state, rec_res, timeCnt, lastTimeCnt):
    valid=False
    # state ShudouState
    # rec_res list[RecResult]
    rec_res = getMaxConfResult(rec_res)
    if state.state == LogicState.LOADINGCOMPLETE:
        state.state = LogicState.INITIALSTATE
        state.init()
        valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
        print(
            "装车完毕->初始状态，时间:", convert_seconds_to_minutes(timeCnt / secondCnt)
        )
        return state, lastTimeCnt
    if state.state == LogicState.CARRYING or state.state == LogicState.READYTOLOAD:

        if len(rec_res) == 2:  # and rec_res[0].y > rec_res[1].y:
            if state.state == LogicState.CARRYING:
                state.state = LogicState.READYTOLOAD
                valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                print(
                    "有土->准备装车，时间:",
                    convert_seconds_to_minutes(timeCnt / secondCnt),
                )

        elif (
            len(rec_res) == 1
            and rec_res[0].label[:5] == "Truck"
            and rec_res[0].y - rec_res[0].h / 2 > state.douY
            # and rec_res[0].get_invlove(state.douX)
        ):
            if state.state == LogicState.CARRYING:
                state.state = LogicState.READYTOLOAD
                valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                print(
                    "有土->准备装车(只有车没斗)，时间:",
                    convert_seconds_to_minutes(timeCnt / secondCnt),
                )

    if state.state == LogicState.READYTOLOAD:
        if len(rec_res) == 2:
            state.disCnt += 1
            if state.disCnt == 1:
                state.rec = rec_res
            else:
                state.disCnt = 0
                if get_close_to(state.rec, rec_res) == -1:
                    state.state = LogicState.LOADINGDOUBT
                    valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                    print(
                        "准备装车中 距离远离->疑似装车，时间:",
                        convert_seconds_to_minutes(timeCnt / secondCnt),
                    )
                    state.init()
        elif len(rec_res) == 1:
            if rec_res[0].label[:5] != "truck":
                state.noTruckCnt += 1
                if state.noTruckCnt >= 2:
                    state.state = LogicState.LOADINGDOUBT
                    valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                    print(
                        "准备装车中 无货车->疑似装车，时间:",
                        convert_seconds_to_minutes(timeCnt / secondCnt),
                    )
                    state.init()
        

    bucketState = get_dou_state(rec_res)
    bucketY = get_douY(rec_res)
    if bucketY != -1:
        state.doUY = bucketY
    if bucketState == 1:
        # 竖斗
        state.verticalCnt += 1
        state.horizontalCnt = 0
        if state.state == LogicState.INITIALSTATE:
            if state.verticalCnt >= 2:
                state.state = LogicState.DIGGING
                valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                print(
                    "初始状态->挖掘中，时间:",
                    convert_seconds_to_minutes(timeCnt / secondCnt),
                )
                state.init()
        elif state.state == LogicState.CARRYING:
            if state.verticalCnt >= 4:
                state.state = LogicState.INITIALSTATE
                # state.shudouCnt+=1
                valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                print(
                    "有土->初始状态，时间:",
                    convert_seconds_to_minutes(timeCnt / secondCnt),
                )
                state.init()
        elif state.state == LogicState.LOADINGDOUBT:
            valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
            if state.verticalCnt >= 2 and timeCnt - lastTimeCnt > 24:
                state.state = LogicState.LOADINGCOMPLETE
                state.shudouCnt += 1
                valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                print(
                    "疑似装车->装车完毕 总数+1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
                    state.shudouCnt,
                    "，时间:",
                    convert_seconds_to_minutes(timeCnt / secondCnt),
                )
                # print("上一次时间:", convert_seconds_to_minutes(lastTimeCnt / secondCnt))
                lastTimeCnt = timeCnt
                state.init()
        elif state.state == LogicState.DIGGING:
            valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                
                
    elif bucketState == 0:
        state.verticalCnt = 0
        state.horizontalCnt += 1
        if state.state == LogicState.DIGGING or state.state == LogicState.LOADINGDOUBT:
            if state.horizontalCnt >= 2:
                state.state = LogicState.CARRYING
                valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
                print("有土，时间:", convert_seconds_to_minutes(timeCnt / secondCnt))
                state.init()
        
        elif state.state == LogicState.CARRYING:
            valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
        # elif state.state == LogicState.LOADINGDOUBT:
        #     valid=True#加载每一个状态转移上，形如 装车完毕->初始状态
    
    if valid==False and len(rec_res)>0:
        print("valid fase time",convert_seconds_to_minutes(timeCnt / secondCnt))
        print("valid fase state",state.state)
        print("valid fase bucket state ",bucketState)
        print("valid fase res",len(rec_res))
        #打印rec_res中每一个元素
        for i in rec_res:
            print(i.label)
        
            

    return state, lastTimeCnt



def TransState(state, rec_res, timeCnt, lastTimeCnt):
    # state ShudouState
    # rec_res list[RecResult]
    rec_res = getMaxConfResult(rec_res)
    bucketState = get_dou_state(rec_res)

    # 修改后的计数逻辑
    if bucketState == 1:  # 竖斗
        state.verticalCnt += 1
        #state.horizontalCnt = 0  # 每次竖斗计数时重置横斗计数
        print("竖斗次数:", state.verticalCnt)
    elif bucketState == 0:  # 横斗
        state.horizontalCnt += 1
        state.verticalCnt = 0  # 每次横斗计数时重置竖斗计数 必须是横斗后面接着连续的竖斗
        print("横斗次数:", state.horizontalCnt)

    # 当横斗达到5次且竖斗达到5次时，装车次数加一 trans1
    if state.verticalCnt >= 4 and state.horizontalCnt >= 4:
        state.shudouCnt += 1
        print(
            "达到4次横斗和4次竖斗，总数+1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
            state.shudouCnt,
            "，时间:",
            convert_seconds_to_minutes(timeCnt / secondCnt),
        )
        # 重置计数器
        state.verticalCnt = 0
        state.horizontalCnt = 0

    return state, lastTimeCnt

