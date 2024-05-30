import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from astropy.io import fits
import warnings
warnings.filterwarnings('ignore')


# Position and Magnification Plots

def error_plot(filename_1, filename_2, filename_4, filename_5, plot_name):
    # Storage for parsed data
    data = []
    
    val = pd.read_csv(filename_4)
    val.__dataframe__
    val_column = val.columns[0]

    # Split the values in the data_column and expand into separate columns
    val = val[val_column].str.split(expand=True)

    # Convert the DataFrame to numeric type
    val = val.apply(pd.to_numeric)

    # Line by line read (Remove # from obs file)
    with open(filename_1, 'r') as file:
        for line in file:
            # Skip lines starting with "#"
            if line.startswith("#"):
                continue
            
            # Split the line by whitespace
            line_data = line.split()
            
            # Remove # 
            line_data = [float(val) for val in line_data if val != '#']  
            
            data.append(line_data)
    
    # Convert to DataFrame
    data_df = pd.DataFrame(data)

    # Exclude the first row
    data_df = data_df.iloc[1:]

    data_df.insert(8, "Label", ['A','B','C','D'], True)

    data_df = data_df.drop(columns =[3, 5, 6, 7])

    # Read and process the predicted data
    data_pred = pd.read_csv(filename_2, header=None, delim_whitespace=True, comment='#')
    df_pred = data_pred.iloc[1:]

    # Function for swapping data 
    def swap_rows(df, row1, row2):
        df.iloc[row1], df.iloc[row2] =  df.iloc[row2].copy(), df.iloc[row1].copy()
        return df
    
    # For loop to iterate over row range for row swapping
    for i in range(4):
        diff = abs(abs(data_df.iloc[i,0]) - abs(df_pred[0]))
        m = diff.idxmin()
        n = min(diff)
        if n < 0.01:
            df_pred = swap_rows(df_pred, i, (m-1))
        else:
            continue
        
    df_pred = df_pred.drop(columns =[3])

    # Eliminating the 5th image
    if len(df_pred[2])>4:
        min_vales = np.min(abs(df_pred[2]))
        df_2 = abs(df_pred)
        b = df_2.index.get_loc(df_2[df_2[2] == min_vales].index[0])
        df_3 = df_2.drop(b, axis='index')
        df_pred = df_3

    # Calculations for Position Error values
    d_x = data_df[0]-df_pred[0]
    d_y = data_df[1]-df_pred[1]
    sum_sq = (d_x**2) + (d_y**2)
    sq = np.sqrt(sum_sq)
    rms = np.average(sq)
    rms_unit = rms*1000
    rms_round = round(rms_unit, 3)
    rms_str = str(rms_round)

    # Plotting Position Error Graph
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(style="ticks", rc=custom_params)

    colours1 = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    colours = [(0.1,0.4,1.0,0.7), (0.0,0.7,0.4,0.7), (0.7,0.3,0.4,0.7), (0.8,0.7,0.1,0.7)]
    plt.figure(figsize =(8,6))
    plt.bar(data_df['Label'], sq, label=data_df['Label'], color = colours1)
    plt.axhline(xmin=0.05, xmax=0.23, y=3*sq[1], linestyle ='--', color ='k', linewidth = 2)
    plt.axhline(xmin=0.29, xmax=0.47, y=3*sq[2], linestyle ='--', color ='k', linewidth = 2)
    plt.axhline(xmin=0.53, xmax=0.71, y=3*sq[3], linestyle ='--', color ='k', linewidth = 2)
    plt.axhline(xmin=0.77, xmax=0.95, y=3*sq[4], linestyle ='--', color ='k', linewidth = 2)
    plt.title('SIE Pos Constraint' + ',  ' + '$Δ^{RMS} _{Pos}$ = ' + rms_str + ' mas')
    plt.legend(labels=['_', '_', '_', '_', '3 σ Error'])
    plt.xlabel('Image')
    plt.ylabel('Error')
    plt.show()

    # Calculations for Magnification value
    f = df_pred[2][1]
    flux = df_pred[2]/f
    df_pred[3] = flux 

    df_pred[3] = abs(df_pred[3])

    # Create data 
    x = np.arange(4)
    width = 0.3

    # FITS image processing for predicted flux at observed positions 
    image = fits.open(filename_5)
    values = image[0].data
    image.close()
    dat = values[6]
    g = data_df[0]*100
    h = data_df[1]*100

    x_pos = 350 + g
    y_pos = 350 + h

    x_pos = x_pos.astype(int)
    y_pos = y_pos.astype(int)

    flux_pos = []

    for i in range(1,5):
        flux_cal = dat[x_pos[i]][y_pos[i]]
        flux_pos.append(flux_cal)

    l = flux_pos[0]
    true_flux = flux_pos/l
    true_flux = abs(true_flux)

    # Plotting Flux Error Graph
    plt.figure(figsize =(8,6))
    plt.bar(x-0.15, val[0], width, color='cyan', edgecolor ='k') 
    plt.bar(x+0.15, df_pred[3], width, color='red', edgecolor='k') 
    plt.bar(x+0.45, true_flux, width, color='green', edgecolor='k')
    plt.errorbar(x-0.15, val[0], yerr=3*(val[1]), fmt='o', color='black', capsize=4, label='3 σ Error')
    plt.xticks(x+0.15, data_df['Label']) 
    plt.xlabel("Image") 
    plt.ylabel("Flux Ratio") 
    plt.legend(labels=['Observed Flux Ratio', 'Predicted Flux Ratio', 'Predicted Flux at Observed Positions', '3 σ Error'])
    plt.title(plot_name + ' Flux Ratio Error')
    plt.show() 


    return data_df, df_pred



# Critical Curves Plot

def critcurve_plot(filename_1, filename_2, filename_3, plot_name):
    data_crit = pd.read_csv(filename_3, header= None, sep="\s+")
    data_crit.__dataframe__
    df = data_crit.iloc[1:]

    # Initialize empty list 
    data = []
    
    # Line by line checking
    with open(filename_1, 'r') as file:
        for line in file:
            # Skip lines starting with #
            if line.startswith("#"):
                continue
            
            # Split by space
            line_data = line.split()
            
            # Remove #
            line_data = [float(val) for val in line_data if val != '#']  # Exclude '#' characters
            
            data.append(line_data)
    
    # Convert the list of lists to a DataFrame
    data_df = pd.DataFrame(data)

    # Exclude the first row
    data_df = data_df.iloc[1:]

    # Read and process the predicted data
    de = pd.read_csv(filename_2, header=None, delim_whitespace=True, comment='#')
    de = de.iloc[1:]

    # Function for swapping data 
    def swap_rows(df, row1, row2):
        df.iloc[row1], df.iloc[row2] =  df.iloc[row2].copy(), df.iloc[row1].copy()
        return df
    
    # For loop to iterate over row range for row swapping
    for i in range(4):
        diff = abs(abs(de.iloc[i,0]) - abs(de[0]))
        m = diff.idxmin()
        n = min(diff)
        if n < 0.01:
            de = swap_rows(de, i, (m-1))
        else:
            continue
        
    de = de.drop(columns =[3])

    # Eliminating the 5th image
    if len(de[2])>4:
        min_vales = np.min(abs(de[2]))
        df_4 = abs(de)
        b = df_4.index.get_loc(df_4[df_4[2] == min_vales].index[0])
        df_5 = df_4.drop(b, axis='index')
        de = df_5

    labels = ['A', 'B', 'C', 'D']

    # Plotting Critial Curves
    plt.figure(figsize=(8, 8))
    plt.scatter(df[0]*100, df[1]*100, s=4)
    plt.scatter(df[2]*100, df[3]*100, s=4)
    plt.scatter(df[4]*100, df[5]*100, s=4)
    plt.scatter(df[6]*100, df[7]*100, s=4)

    # Plotting obs image positions and labels 
    plt.scatter(data_df[0]*100, data_df[1]*100, s=15, color = 'blue', label = 'Observed Position')
    plt.scatter(de[0]*100, de[1]*100, s = 180, marker= '+', label = 'Predicted Position', color = 'orange')
    for x, y, txt in zip(data_df[0]*100, data_df[1]*100, labels):
        plt.text(x, y-17, txt, fontsize=13, ha='center', va='bottom')

    plt.title(plot_name + ' Critical Curves')
    plt.legend()
    plt.xlabel('x [pixel]')
    plt.ylabel('y [pixel]')
    plt.xlim(-170,170)
    plt.ylim(-170,170)
    plt.show()
    
    return data_df, df
