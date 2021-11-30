import matplotlib.pyplot as plt
from ..Structures import Indicator

def CandleChart(ohlcv, indicators=None, tradehist=None):
    data = ohlcv.df
    subplotli = [5,2]
    mainindic = []
    subindic = []
    if indicators:
      if type(indicators)==list:
        for i in indicators:
          if i._plotsetting() == 'sub':
            subplotli.append(2)
            subindic.append(i)
          elif i._plotsetting() == 'main':
            mainindic.append(i)
      else:
        raise ValueError('Wrong Indicators')

    fig, axs = plt.subplots(
        len(subplotli),
        1,
        sharex=True,
        gridspec_kw={'height_ratios': subplotli},
        dpi=200,
        figsize=(0.4 * (12 + 4 * (len(subplotli) - 1) * 0.6),
                 0.4 * (0.75 * (12 + 4 * (len(subplotli) - 1) * 0.6))))

    axs[0].tick_params(axis='x', labelsize=3, rotation=90)
    fig.suptitle(f"{data['code'][0]} - CandleChart")

    fig.figsize = [10, 7.5]
    minc = data['low'].min()
    maxc = data['high'].max()
    axs[0].set_ylim(minc - (maxc - minc) / 3.5, maxc + (maxc - minc) / 6)

    posdat = data[data['open'] < data['close']]
    negdat = data[data['open'] >= data['close']]

    inter = (data.index[1] - data.index[0])* 0.9
    axs[0].grid(zorder=0)
    axs[0].vlines(x=posdat.index,
                ymin=posdat['low'],
                ymax=posdat['high'],
                color='red', alpha=1, lw=0.5,zorder=5)

    axs[0].vlines(x=negdat.index,
                ymin=negdat['low'],
                ymax=negdat['high'],
                color='blue', alpha=1, lw=0.5,zorder=5)

    axs[0].bar(x=posdat.index,
            bottom=posdat['open'],
            height=posdat['close'] - posdat['open'],
            color='red',alpha=1,
            width=inter, edgecolor='white',linewidth=0,zorder=3)
    axs[0].bar(x=negdat.index,
            bottom=negdat['close'],
            height=negdat['open'] - negdat['close'],
            color='blue', alpha=1,
            width=inter,edgecolor='white',linewidth=0,zorder=3)
    axs[0].ticklabel_format(axis='y', style='plain')

    #Volume
    posvol = data[data['open'] < data['close']]['volume']
    negvol = data[data['open'] >= data['close']]['volume']

    axs[1].set_ylim(
        0, data['volume'][data['volume'] < (
            data['volume'].mean() + data['volume'].std() * 1.98)].max()*3)
    axs[1].bar(x=posvol.index,
                height=posvol,
                color='red', alpha=0.7,
                width=inter)
    axs[1].bar(x=negvol.index,
                height=negvol,
                color='blue', alpha=0.7,
                width=inter)

    axs[1].ticklabel_format(axis='y', style='plain')
    

    
    if indicators:
      for k in mainindic:
        indi = k(df=data)
        indi.draw(axs=axs[0])

      for k in range(len(subindic)):
        indi = subindic[k](df=data)
        indi.draw(axs=axs[k+2])

    for a in axs:
      a.legend(loc='best', fontsize=3)
      a.tick_params(axis='y', labelsize=3)

    axs[-1].tick_params(axis='x', labelsize=3, rotation=90)
    plt.show()