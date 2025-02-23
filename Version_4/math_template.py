import numpy as np
import math

def pose_to_matrix(pose):
    """
    將 (x, y, theta)（其中 theta 為角度單位）轉換成 3x3 齊次變換矩陣
    """
    x, y, theta_deg = pose
    theta = math.radians(theta_deg)  # 角度轉弧度
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    return np.array([
        [cos_theta, -sin_theta, x],
        [sin_theta,  cos_theta, y],
        [0,         0,         1]
    ])

def matrix_to_pose(matrix):
    """
    從 3x3 齊次變換矩陣中提取 (x, y, theta)，其中 theta 為角度單位
    """
    x = matrix[0, 2]
    y = matrix[1, 2]
    theta = math.atan2(matrix[1, 0], matrix[0, 0])
    return (x, y, math.degrees(theta))  # 弧度轉角度

def compute_pose(pose_AB, pose_BC):
    """
    根據已知的 A->B 與 B->C 的變換，計算 A->C 的變換。
    輸入與輸出之角度皆為度。
    """
    T_AB = pose_to_matrix(pose_AB)
    T_BC = pose_to_matrix(pose_BC)
    # 從 A 到 C 的變換矩陣為 T_AC = T_AB * T_BC
    T_AC = np.dot(T_AB, T_BC)
    return matrix_to_pose(T_AC)

if __name__ == "__main__":
    # 範例數據：假設 AB 變換為 (1, 2, 30°) ，BC 變換為 (3, 4, 45°)
    pose_AB = (1, 1, 0)
    pose_BC = (3, 4, 30)
    
    pose_AC = compute_pose(pose_AB, pose_BC)
    print("A 到 C 的相對位移和朝向 (x, y, theta [deg]):")
    print(pose_AC)