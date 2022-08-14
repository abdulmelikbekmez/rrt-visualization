def normalize_angle(angle: float) -> float:
    if angle > 180:
        return angle - 360
    elif angle < -180:
        return angle + 360
    return angle
