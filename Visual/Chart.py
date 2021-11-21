import matplotlib.pyplot as plt

def CandleChart(data, show='auto', tradehist=None):
    subplotli = [5]    
    print(data)
    fig, axs = plt.subplots(
        len(subplotli),
        1,
        sharex=True,
        gridspec_kw={'height_ratios': subplotli},
        dpi=200,
        figsize=(0.4 * (12 + 4 * (len(subplotli) - 1) * 0.6),
                 0.4 * (0.75 * (12 + 4 * (len(subplotli) - 1) * 0.6))))

    plt.xticks(rotation=90, fontsize=3)
    plt.grid(True)

    fig.suptitle(f"{data['code'][0]} - SimplePlot")

    fig.figsize = [10, 7.5]
    minc = data['low'].min()
    maxc = data['high'].max()
    axs.set_ylim(minc - (maxc - minc) / 3.5, maxc + (maxc - minc) / 6)

    posdat = data[data['open'] < data['close']]
    negdat = data[data['open'] >= data['close']]

    inter = data.index[1] - data.index[0]

    axs.vlines(x=posdat.index,
                ymin=posdat['low'],
                ymax=posdat['high'],
                color='red', alpha=1, lw=0.5)

    axs.vlines(x=negdat.index,
                ymin=negdat['low'],
                ymax=negdat['high'],
                color='blue', alpha=1, lw=0.5)

    axs.bar(x=posdat.index,
            bottom=posdat['open'],
            height=posdat['close'] - posdat['open'],
            color='red',alpha=1,
            width=inter)
    axs.bar(x=negdat.index,
            bottom=negdat['close'],
            height=negdat['open'] - negdat['close'],
            color='blue', alpha=1,
            width=inter)
    axs.ticklabel_format(axis='y', style='plain')

    #Volume
    posvol = data[data['open'] < data['close']]['volume']
    negvol = data[data['open'] >= data['close']]['volume']
    volaxs = axs.twinx()
    volaxs.set_ylim(
        0, data['volume'][data['volume'] < (
            data['volume'].mean() + data['volume'].std() * 1.98)].max() *
        6)
    volaxs.bar(x=posvol.index,
                height=posvol,
                color='red', alpha=0.7,
                width=inter)
    volaxs.bar(x=negvol.index,
                height=negvol,
                color='blue', alpha=0.7,
                width=inter)
    volaxs.set_yticklabels([])

    axs.legend(loc='best')

    plt.show()


def SimplePlot(data, show='auto', tradehist=None):
    subplotli = [5]
    subplotlist = ['base']
    zeroone = False
    zerohundred = False
    tradehisted = False

    if tradehist:
        tradehisted = True

    if show == 'auto':
        for i in data.columns:
            #0 ~ 1사이 값
            if i in ['pb']:
                zeroone = True
            #0 ~ 100사이 값
            elif i in ['mfi', 'pk', 'pd']:
                zerohundred = True

    if zeroone:
        subplotli.append(1)
        subplotlist.append('zeroone')
    if zerohundred:
        subplotli.append(1)
        subplotlist.append('zerohundred')
    if tradehisted:
        subplotli.append(1)
        subplotlist.append('tradehist')

    fig, axs = plt.subplots(len(subplotli),
                            1,
                            sharex=True,
                            dpi=100,
                            gridspec_kw={'height_ratios': subplotli},
                            figsize=(12 + 4 * (len(subplotli) - 1) * 0.6,
                                     0.75 * (12 + 4 *
                                             (len(subplotli) - 1) * 0.6)))
    fig.suptitle(f"{data['code'][0]} - SimplePlot")

    if len(subplotli) == 1:
        fig.figsize = [4, 3]

        #Volume
        posvol = data[data['open'] < data['close']]['volume']
        negvol = data[data['open'] >= data['close']]['volume']
        volaxs = axs.twinx()
        volaxs.set_ylim(
            0, data['volume'][data['volume'] < (
                data['volume'].mean() + data['volume'].std() * 1.98)].max() *
            6)
        volaxs.bar(x=posvol.index,
                   height=posvol,
                   color='red',
                   width=0.05 / data.shape[0])
        volaxs.bar(x=negvol.index,
                   height=negvol,
                   color='blue',
                   width=0.05 / data.shape[0])
        volaxs.set_yticklabels([])

        #close
        minc = data['close'].min()
        maxc = data['close'].max()
        axs.set_ylim(minc - (maxc - minc) / 3.5, maxc + (maxc - minc) / 6)
        axs.plot(data.index, data['close'], color='black', label='close')
        axs.ticklabel_format(axis='y', style='plain')

        axs.legend(loc='best')

    else:
        minc = data['close'].min()
        maxc = data['close'].max()
        axs[0].set_ylim(minc - (maxc - minc) / 3.5, maxc + (maxc - minc) / 6)
        axs[0].plot(data.index, data['close'], color='black', label='close')
        axs[0].ticklabel_format(axis='y', style='plain')

        posvol = data[data['open'] > data['close']]['volume']
        negvol = data[data['open'] <= data['close']]['volume']
        volaxs = axs[0].twinx()
        volaxs.set_ylim(
            0,
            data.drop(data[data['volume'] > (
                data['volume'].mean() + data['volume'].std() * 1.98)]).max() *
            6)
        volaxs.bar(posvol.index, posvol, color='red', width=0.4)
        volaxs.bar(negvol.index, negvol, color='blue', width=0.4)
        volaxs.set_yticklabels([])

        if show == 'auto':
            for i in data.columns:
                if not i in [
                        'open', 'high', 'low', 'volume', 'code', 'close', 'bw',
                        'profits'
                ]:
                    #base - bb
                    if i in ['upper', 'lower']:
                        axs[0].fill_between(data.index,
                                            data['upper'],
                                            data['lower'],
                                            alpha=0.15)
                        axs[0].plot(data.index, data[i], label=i)

                    #zeroone

                    elif i in ['pb']:
                        index = 0
                        for k in range(len(subplotlist)):
                            if subplotlist[k] == 'zeroone':
                                index = k

                        axs[index].plot(data.index, data[i], label=i)

                    #zerohundred
                    elif i in ['mfi', 'pk', 'pd']:
                        index = 0
                        for k in range(len(subplotlist)):
                            if subplotlist[k] == 'zerohundred':
                                index = k
                        axs[index].plot(data.index, data[i], label=i)

                    elif i in ['ports']:
                        index = 0
                        for k in range(len(subplotlist)):
                            if subplotlist[k] == 'tradehist':
                                index = k
                        axs[index].ticklabel_format(axis='y', style='plain')
                        axs[index].plot(data.index, data[i], label=i)
                    #base
                    else:
                        axs[0].plot(data.index, data[i], label=i)

            if tradehisted:
                axs[0].plot(data.index[0],
                            0,
                            marker='^',
                            color='green',
                            label='buy',
                            markersize=6)
                axs[0].plot(data.index[0],
                            0,
                            marker='v',
                            color='orange',
                            label='sell',
                            markersize=6)
                axs[0].plot(data.index[0],
                            0,
                            marker='*',
                            color='black',
                            markersize=10)
                for h in tradehist:
                    if h[1] == 'buy':
                        axs[0].plot(h[0],
                                    h[2],
                                    marker='^',
                                    color='green',
                                    markersize=6)
                    elif h[1] == 'sell':
                        axs[0].plot(h[0],
                                    h[2],
                                    marker='v',
                                    color='orange',
                                    markersize=6)

            for ax in axs:
                ax.legend(loc='best')
                ax.ticklabel_format(axis='y', style='plain')

    plt.show()
