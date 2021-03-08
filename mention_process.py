import pandas as pd
import re
import datetime


def mentioned(df):
    mentions = []
    for item in df.iterrows():
        match = re.findall('@[A-Za-z0-9_:]+\s',item[1][2])
        if match:
            mentions.append(match)
        else:
            mentions.append('NAN')

    df['Mention'] = mentions
    df.created_at = pd.to_datetime(df.created_at)
    start_date = datetime.datetime.now() - datetime.timedelta(30)
    lastdayfrom = pd.to_datetime(start_date)

    #set index from column Date
    df = df.set_index('created_at')
    #if datetimeindex isn't order, order it
    df= df.sort_index()

    #last 30 days of date lastday
    df_30days = df.loc[lastdayfrom:].reset_index()

    listofdics = []
    for item in df_30days.iterrows():
        if item[1][3] == 'NAN':
            pass
        else:
            for i in item[1][3]:
                data = df_30days.iloc[item[0], :3].to_dict()
                data['Mention'] = i
                listofdics.append(data)

    newdf = pd.DataFrame(listofdics)
    newdf.Mention = newdf.Mention.apply(lambda x: x.replace(':', ''))
    newdf['@Mention'] = newdf['Mention']
    newdf['Number Mentions'] = newdf.Mention.apply(lambda x: f'Mentioned {newdf[newdf.Mention == x].Mention.value_counts().to_list()[0]} time/times in 30 days')
    final_df = newdf.iloc[:, 2:]
    return final_df


if __name__ == '__main__':
    mentioned(df)