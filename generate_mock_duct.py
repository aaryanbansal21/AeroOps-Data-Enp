import os
import numpy as np

def generate_duct_ply(filename, length=20.0, radius=1.0, num_points=80000):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Mathematically generate points along a cylinder (representing the duct)
    theta = np.random.uniform(0, 2 * np.pi, num_points)
    z = np.random.uniform(0, length, num_points)
    
    # Add slight noisy perturbation to radius to simulate metallic unevenness or dust accumulation
    r_noise = radius + np.random.normal(0, 0.02, num_points)
    
    x = r_noise * np.cos(theta)
    y = r_noise * np.sin(theta)
    
    # Write to standard PLY format (ASCII for simplicity and ease of debugging)
    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {num_points}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        
        for i in range(num_points):
            # Base color grey (metal), add some randomized noise for visual texture
            color = int(np.clip(130 + np.random.normal(0, 25), 0, 255))
            f.write(f"{x[i]:.4f} {y[i]:.4f} {z[i]:.4f} {color} {color} {color}\n")

if __name__ == "__main__":
    filepath = "static/maps/mock_duct.ply"
    generate_duct_ply(filepath)
    print(f"Successfully generated a 3D cylindrical point cloud at {filepath}")
