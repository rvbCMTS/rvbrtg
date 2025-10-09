import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pydicom


def check_axial_alignment(dcm_file, mode='plot', scale_n=25):
    # image orientation pat
    IO = np.asarray(dcm_file.ImageOrientationPatient)
    # Image position patient
    IP = np.asarray(dcm_file.ImagePositionPatient)
    # pixel spacing
    pixel_spacing = np.asarray(dcm_file.PixelSpacing)
    di, dj = pixel_spacing[0], pixel_spacing[1]
    rows, cols = dcm_file.Rows, dcm_file.Columns

    Mat = np.array(
        [
            [IO[0] * di, IO[3] * dj, 0, IP[0]],
            [IO[1] * di, IO[4] * dj, 0, IP[1]], 
            [IO[2] * di, IO[5] * dj, 0, IP[2]],
            [         0,          0, 0,    1],
        ]
    )

    normal_P = np.cross(IO[0:3], IO[3:6])
    normal_G = np.cross([1,0,0], [0,1,0])
    
    
    normal_alignment = np.abs(np.dot(normal_P, normal_G))

    if mode == 'calc_alignment':
        return normal_alignment
    

    datas = []
    Gx, Gy, Gz = [], [], []
    Px, Py, Pz = [], [], []

    for i in [0, rows - 1]:
        for j in [0, cols - 1]:
            # image space
            Gx.append(di*i), Gy.append(dj*j), Gz.append(0)
            # RCS space
            P = np.matmul(Mat, np.array([i,j,0,1]).T)
            Px.append(P[0]), Py.append(P[1]), Pz.append(P[2]) 

    datas = []

    cG = np.array([di * (rows - 1) / 2, dj * (cols - 1) / 2, 0])
    cP = np.matmul(Mat, np.array([rows/2,cols/2,0,1]).T)

    G_plane = go.Mesh3d(
        x=Gx, y=Gy, z=Gz,
        i=[0, 0, 0, 1], j=[1, 2, 3, 2], k=[2, 3, 1, 3],
        opacity=0.25, name='Image space', color='red', delaunayaxis='z')
    
    P_plane = go.Mesh3d(
        x=Px, y=Py, z=Pz,
        i=[0, 0, 0, 1], j=[1, 2, 3, 2], k=[2, 3, 1, 3],
        opacity=0.25, name='RCS space', color='blue', delaunayaxis='z')

    datas.append(P_plane)
    datas.append(G_plane)
    
    # plot origin
    o_size = 100
    datas.append(go.Scatter3d(
        x=[0, +o_size], y=[0, 0], z=[0, 0],
        mode='lines', showlegend=False, line=dict(color='black')))
    
    datas.append(go.Scatter3d(
        x=[0, 0], y=[0, +o_size], z=[0, 0],
        mode='lines', showlegend=False, line=dict(color='black')))
    
    datas.append(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[0, +o_size],
        mode='lines', showlegend=False, line=dict(color='black')))

    # plot normal vectors
    datas.append(
        go.Scatter3d(
            x=[cP[0], cP[0] + scale_n * normal_P[0]],
            y=[cP[1], cP[1] + scale_n * normal_P[1]],
            z=[cP[2], cP[2] + scale_n * normal_P[2]], 
            mode='lines', name='normal', showlegend=False,
            line=dict(color='blue', width=5)))

    datas.append(
        go.Scatter3d(
            x=[cG[0], cG[0] + scale_n * normal_G[0]],
            y=[cG[1], cG[1] + scale_n * normal_G[1]],
            z=[cG[2], cG[2] + scale_n * normal_G[2]], 
            mode='lines', name='normal', showlegend=False,
            line=dict(color='red', width=5)))

    datas.append(
        go.Scatter3d(
            x=[IP[0]], y=[IP[1]], z=[IP[2]], 
            mode='markers', name='IPP (RCS space)', line=dict(color='blue', width=5)))
    datas.append(
        go.Scatter3d(
            x=[0], y=[0], z=[0], 
            mode='markers', name='IPP (image space)', line=dict(color='red', width=5)))


    fig = go.Figure(data=datas)

    fig.update_layout(
        scene=dict(
            xaxis_title='x / mm',
            yaxis_title='y / mm',
            zaxis_title='y / mm',
        ),
    )

    return fig.show()