import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
sns.set_theme(style="ticks",font_scale=1.5)

def get_stuff(path):
    """
    MEFFMASS(ALL)=YES must be defined
    path -> .f06 file
    """
    
    cont={"Mod":[],"freq":[],"T1":[],"T2":[],"T3":[],"R1":[],"R2":[],"R3":[]}
    with open(path,"r") as fin:
        lines=fin.readlines()
        for i,line in enumerate(lines):
            if "FOR TRANSLATIONAL DEGREES OF FREEDOM" in line:
                idx=i
                while True:
                    if lines[idx+5].strip()=="": break
                    cont["Mod"].append(int(lines[idx+5].split()[0]))
                    cont["freq"].append(float(lines[idx+5].split()[1]))
                    cont["T1"].append(float(lines[idx+5].split()[2]))
                    cont["T2"].append(float(lines[idx+5].split()[4]))
                    cont["T3"].append(float(lines[idx+5].split()[6]))
                    idx+=1                
                    
            elif "FOR ROTATIONAL DEGREES OF FREEDOM" in line:
                idx=i
                while True:
                    if lines[idx+5].strip()=="": break
                    cont["R1"].append(float(lines[idx+5].split()[2]))
                    cont["R2"].append(float(lines[idx+5].split()[4]))
                    cont["R3"].append(float(lines[idx+5].split()[6]))
                    idx+=1
    return cont



def plot_stuff(cont,no_modes=10):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    
    df=pd.DataFrame(cont).head(no_modes)
    df.set_index("Mod",inplace=True)
    df_cont=df.drop(["freq"],axis=1).T
    
    df_cont.plot(kind="barh",stacked=True, ax=axes[0])
    axes[0].legend(title="Modes",bbox_to_anchor=(-0.3, 0),loc='lower left')
    axes[0].set_xlabel("Modal Contribution")
    axes[0].set_xlim(0, 1.01)
    
    df["freq"].plot(kind="bar",ax=axes[1],color="gray")
    axes[1].set_ylabel("Frequency (Hz)")
    
    plt.suptitle(f"File: {file_name} ({no_modes} modes)", color="crimson")
    plt.show()


if __name__=="__main__":
    path=r'/basic.f06'
    
    folder=os.path.dirname(path)
    file_name=os.path.split(path)[-1].split(".")[0]
    os.chdir(folder)
    
    ll=get_stuff(path)
    plot_stuff(ll)
