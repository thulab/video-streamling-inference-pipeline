import StateTransition
import LogicState
import Reconization
import detect_o
import sys

# model_path = "yolo5.pt"
model_path = "../yolo9.pt"


def shudouMain(video_path):
    print(video_path)
    opt = detect_o.parse_opt()

    device = detect_o.select_device(opt.device)
    model = detect_o.load_model(model_path, device, "truck.yaml", opt.dnn)
    stride, names, pt, jit, onnx, engine = (
        model.stride,
        model.names,
        model.pt,
        model.jit,
        model.onnx,
        model.engine,
    )
    imgsz = detect_o.check_img_size(opt.imgsz, s=stride)  # check image size

    # Load image
    dataset = detect_o.load_image(video_path, img_size=imgsz, stride=stride, auto=pt)

    # Run inference
    results = detect_o.run_inference(
        model,
        dataset,
        opt.conf_thres,
        opt.iou_thres,
        opt.classes,
        opt.agnostic_nms,
        opt.max_det,
    )

    shudouState = LogicState.ShudouState()
    # Print results
    timeCnt = 0
    lastTimeCnt = 0
    cnt = 0
    tmpr = []
    for r in results:
        cnt += 1
        if cnt % 10 != 0:
            for rr in r:
                tmpr.append(rr)
            continue
        else:
            cnt = 0
        timeCnt += 1
        # if timeCnt % 30 == 0:
        #     print(f"时间: {StateTransition.convert_seconds_to_minutes(timeCnt / 3)}")
        #     # print("time:", timeCnt/3)
        nr = []
        # for rr in r:
        for rr in tmpr:
            cls, x, y, w, h, conf = rr
            nr.append(Reconization.RecResult(x, y, w, h, names[int(cls)], conf))
        shudouState, lastTimeCnt = StateTransition.TransState(
            shudouState, nr, timeCnt, lastTimeCnt
        )
        if cnt == 0:
            tmpr = []
        # cls, x, y, w, h, conf = r
        # print(
        #     f"{names[int(cls)]}: {conf:.2f} - Position: ({x:.2f}, {y:.2f}, {w:.2f}, {h:.2f})"
        # )

    return shudouState.shudouCnt


if __name__ == "__main__":
    with open("output1.txt", "w") as file:
        original_stdout = sys.stdout  # 保存当前的标准输出，以便之后恢复
        sys.stdout = file
        print(shudouMain("../video/wKhvFV_dYPGAWEv5BFT44VydHZg220.mp4"))
        print(shudouMain("../video/wKhvFV_dWeqABDKHBFTb4YHUVh4168.mp4"))  #  38 38     trans1 3横斗4竖斗  40
        print(shudouMain("../video/wKhvFV_dV6eAZHgZBFSlhViP2AQ327.mp4"))  #  35 34     trans1 35
        print(shudouMain("../video/wKhvFV_dVT-AMFZEBFZ94Bofe6g382.mp4"))  #  22 24     trans1 28
        print(shudouMain("../video/wKhvFV_dY0qAEyg-BFUDsXYhoK8719.mp4"))  #  32 36     trans1 39
        print(shudouMain("../video/wKhvFV_dYPGAWEv5BFT44VydHZg220.mp4"))  #  33 33     trans1 34
        # print(shudouMain("../video/wKhvFV_dXp6ABRmCBFS8huFV6Hs991.mp4"))  #  38 29     trans1 43
        print(shudouMain("../video/wKhvFV_dXEWAb-x4BFStnqX7UuU961.mp4"))  #  30 31     trans1 35
        print(shudouMain("../video/wKhvFV_gAbGAFkLmBFSjHctjhrU722.mp4"))  #  30 31     trans1 31
        # print(
        #     shudouMain("../video/wKhvFV_f_2GAPmfZBFY42SwjOfE254.mp4")
        # )  #  4 前面全是废的，最后一两分钟才在挖 9     trans1 9
        #print(shudouMain("../video/wKhvFV_dfQmAAoPjA2DtMyW3GM4652.mp4"))  #  0 在开车 2     trans1 2
        print(shudouMain("../video/wKhvFV_gBn6ACKHwBFS3XnD-3JQ400.mp4"))  #  27 26     trans1 31
        print(shudouMain("../video/wKhvFV_gA9CATbgmBFSOU7kAi5Q293.mp4"))  #  26 20     trans1 21
        #print(shudouMain("../video/wKhvFV_gEBiAR9FIAHivoqHLkic639.mp4"))  #  0 在开车 1     trans1 1
        print(shudouMain("../video/wKhvFV_gD_mAMwlhBFUzqHqUhXI877.mp4"))  #  26 26     trans1 24
        print(shudouMain("../video/wKhvFV_gDZqAK9SjBFURWB8QWy0068.mp4"))  #  24 20     trans1 20
        # print(
        #     shudouMain("../video/wKhvFV_gCtSABOUQBFTs9mliM0I872.mp4")
        # )  #  1 其余的都在平土 4   trans 6
        print(shudouMain("../video/wKhvFV_gCRmAQJfzBFTQa6cjGnY345.mp4"))  #  24 21     trans1 27
        sys.stdout = original_stdout
