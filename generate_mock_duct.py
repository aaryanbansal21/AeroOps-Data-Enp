import os
import random

def is_inside_segment(x, y, z, p1, p2, axis, W):
    """
    Checks if a point is strictly INSIDE the hollow volume of a given duct segment.
    Uses a small epsilon so that points *exactly* on the walls are not deleted.
    """
    EPS = 0.05
    if axis == 0:
        in_x = min(p1[0], p2[0]) - W - EPS < x < max(p1[0], p2[0]) + W + EPS
        in_y = p1[1] - W + EPS < y < p1[1] + W - EPS
        in_z = p1[2] - W + EPS < z < p1[2] + W - EPS
        return in_x and in_y and in_z
    elif axis == 1:
        in_y = min(p1[1], p2[1]) - W - EPS < y < max(p1[1], p2[1]) + W + EPS
        in_x = p1[0] - W + EPS < x < p1[0] + W - EPS
        in_z = p1[2] - W + EPS < z < p1[2] + W - EPS
        return in_y and in_x and in_z
    else:
        in_z = min(p1[2], p2[2]) - W - EPS < z < max(p1[2], p2[2]) + W + EPS
        in_x = p1[0] - W + EPS < x < p1[0] + W - EPS
        in_y = p1[1] - W + EPS < y < p1[1] + W - EPS
        return in_z and in_x and in_y

def generate_random_duct(filename, num_points=150000):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    path = [
        (0, 0, 0),
        (0, 0, 15),       
        (10, 0, 15),      
        (10, 5, 15),      
        (10, 5, 25),      
        (0, 5, 25),       
        (0, 0, 25),       
        (0, 0, 40)        
    ]
    
    segments = []
    total_length = 0
    W = 1.0 
    
    for i in range(len(path)-1):
        p1 = path[i]
        p2 = path[i+1]
        
        if p1[0] != p2[0]: axis = 0; length = abs(p2[0] - p1[0])
        elif p1[1] != p2[1]: axis = 1; length = abs(p2[1] - p1[1])
        else: axis = 2; length = abs(p2[2] - p1[2])
            
        segments.append((p1, p2, axis, length))
        total_length += length

    all_points = []

    # Stage 1: Generate all structural wall points including internal corner overlap
    for p1, p2, axis, length in segments:
        pts_this_seg = int(num_points * (length / total_length))
        
        min_val = min(p1[axis], p2[axis]) - W
        max_val = max(p1[axis], p2[axis]) + W
        
        for _ in range(pts_this_seg):
            t_val = random.uniform(min_val, max_val)
            wall = random.randint(0, 3)
            noise = random.gauss(0, 0.01)
            
            if wall == 0:
                a = random.uniform(-W, W)
                b = W + noise
            elif wall == 1:
                a = random.uniform(-W, W)
                b = -W + noise
            elif wall == 2:
                a = W + noise
                b = random.uniform(-W, W)
            else:
                a = -W + noise
                b = random.uniform(-W, W)
            
            if axis == 0: 
                x = t_val; y = p1[1] + a; z = p1[2] + b
            elif axis == 1: 
                y = t_val; x = p1[0] + a; z = p1[2] + b
            else: 
                z = t_val; x = p1[0] + a; y = p1[1] + b

            base_c = int(max(0, min(255, 140 + random.gauss(0, 15))))
            all_points.append((x, y, z, base_c, base_c, base_c))

    # Stage 2: CSG Boolean Subtraction
    # Delete any points that geometrically fall strictly inside the hollow volume of another connecting tube
    filtered_points = []
    for pt in all_points:
        x, y, z, r, g, b_col = pt
        inside_any = False
        for sg in segments:
            p1_s, p2_s, axis_s, length_s = sg
            # If the point penetrates the interior volume of an intersecting segment, mark it for deletion
            if is_inside_segment(x, y, z, p1_s, p2_s, axis_s, W):
                inside_any = True
                break
        
        if not inside_any:
            filtered_points.append(pt)

    # Stage 3: Write cleanly hollowed map to disk
    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(filtered_points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        
        for pt in filtered_points:
            f.write(f"{pt[0]:.4f} {pt[1]:.4f} {pt[2]:.4f} {pt[3]} {pt[4]} {pt[5]}\n")

if __name__ == "__main__":
    filepath = "static/maps/mock_duct_rect.ply"
    generate_random_duct(filepath, num_points=150000)
    print(f"Successfully generated mathematically hollow connected duct at {filepath}")
