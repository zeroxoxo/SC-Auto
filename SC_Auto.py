#!/usr/bin/python3.6

import soundcloud as sc
import random


token = 'insert_your_access_token'
client_xeno = sc.Client(access_token=token)
me = client_xeno.get('me')

#list of comments
comments = ['ayyyyyyyy', 'nice one :)', 'awesomeeee', 'incredible work dude', 'woah!!!', 'toooo fkn awesome',
            'luv it!', 'awesome!!', 'daaayum', ';D', 'dope one', 'amzng', 'aye', 'soo niiice', 'so good',
            'XDDDDDDDDD', 'dope af', 'nice one', 'XD', 'omfg', 'wow', 'awesomeeee', 'dope', 'incredible',
            '!!!!', '^^', 'WHATTA HELL', 'wooohooooooo', ':DD', 'darn wicked!!!', 'dooope tuuuune!!!!', '=D',
            'outstanding', 'remarkable', 'good work', 'really good!', 'oh man!!', 'yeah!', 'yesh', 'so awesome',
            'dig it', 'smooooth', 'cooool', 'dope', 'sweeet', 'awsm', 'woaaahhhh', 'soo gooood', '<3', 'super hyped',
            'great one', 'yesss', 'next level!!!', 'sick one',  'dope az hell', 'banger!!', 'great work',
            'XD', 'niceee', 'daaayum this is fkn sick man', 'hell yesss', 'dope shit',  'this is pretty sickk',
            'crazy sickkkk', 'this is fkn insane', 'great stuff', 'fresh', 'you rule bro', 'killing it!!', 'omfg!!',
            'fuck yes!!!','fuck yes!!!', 'cool', 'original', 'soooo preeettyyy', 'that is it', 'dat fx'
            'oh, lord', 'amazing, love it', 'epic', 'smoooth', 'oh gosh...', 'loving it', 'niceee', 'awesomeee',
            'great fx', 'wonderful fx', 'top tier sfx', 'nice rhythms', 'quite intence', 'astonishing', 'dat fx though',
            'god damn', 'stunningly', 'breathtakingly', 'rattling', 'real moving stuff', 'quite impressive',
            'lovely', 'top grade', 'top brand', 'pure adoration', 'cool atmo', 'huuuge', 'awsm',
            'aww yess', 'sic1', 'geeenius!!!', 'really vivid', 'paints a pic']


read = open('reject.txt', mode='r')
reject = read.read().split(sep=' ')
read.close()
for i in range(len(reject)-1):
    reject[i] = int(reject[i])
add = open('reject.txt', mode='a')

def sc_iFollow():
    out = []
    i_follow = client_xeno.get('/me/followings/', linked_partitioning=1, limit=200, order='id')
    for f in i_follow.collection:
        out.append(f.id)
    while i_follow.next_href != None:
        i_follow = client_xeno.get(i_follow.next_href, linked_partitioning=1, limit=200, order='id')
        for f in i_follow.collection:
            out.append(f.id)
    return out


def sc_myFollowers():
    out = []
    i_follow = client_xeno.get('/me/followers/', linked_partitioning=1, limit=200, order='id')
    for f in i_follow.collection:
        out.append(f.id)
    while i_follow.next_href != None:
        i_follow = client_xeno.get(i_follow.next_href, linked_partitioning=1, limit=200, order='id')
        for f in i_follow.collection:
            out.append(f.id)
    return out


def sc_iLike():
    out = []
    i_like = client_xeno.get('/me/favorites/', linked_partitioning=1, limit=200, order='id')
    for f in i_like.collection:
        out.append(f.id)
    try:
        while i_like.next_href != None:
            i_like = client_xeno.get(i_like.next_href, linked_partitioning=1, limit=200, order='id')
            for f in i_like.collection:
                out.append(f.id)
    except AttributeError:
        pass
    return out


def sc_Like(id):
    try:
        client_xeno.put('/me/favorites/' + str(id))
    except Exception as e:
        print(str(e))
    return


def sc_postComment(id):
    try:
        x = client_xeno.get('/tracks/%d/' % id).duration
        if int(me.id) != int(id):
            client_xeno.post('/tracks/%d/comments' % id, comment={
                'body': comments.pop(random.randint(0, len(comments))),
                'timestamp': x/random.randint(2, 10)
            })
    except Exception as e:
        print(e)
    return


def sc_Follow(id):
    try:
        client_xeno.put('/me/followings/' + str(id))
    except Exception as e:
        print(str(e))
    return


def sc_Unfollow(id):
    try:
        client_xeno.delete('/me/followings/' + str(id))
        add.write(str(id) + ' ')
    except Exception as e:
        print(str(e))
    return


def sc_FollowFollowers(id):
    print('start sc_FollowFollowers')
    new_follow = client_xeno.get('/users/%d/followers/' % id, limit=200, linked_partitioning=1)
    i_f = sc_iFollow()
    count = 40 + random.randint(0,10)
    x = 0
    j = []
    for i in new_follow.collection:
        if i.id not in i_f and x < count:
            if i.id not in j and i.followers_count >= 120:
                if i.id not in reject:
                    try:
                        t = client_xeno.get('/users/%d/tracks/' % i.id)[0].id
                        sc_Like(t)
                        sc_postComment(t)
                    except:
                        pass
                    print('Followed ' + i.username)
                    j.append(i.id)
                    sc_Follow(i.id)
                    x += 1
        elif x >= count:
            return
    while new_follow.next_href != None:
        new_follow = client_xeno.get(new_follow.next_href, limit=200, linked_partitioning=1)
        for i in new_follow.collection:
            if i.id not in i_f and x < count:
                if i.id not in j and i.followers_count >= 120:
                    if i.id not in reject:
                        try:
                            t = client_xeno.get('/users/%d/tracks/' % i.id)[0].id
                            sc_Like(t)
                            sc_postComment(t)
                        except:
                            pass
                        print('Followed ' + i.username)
                        j.append(i.id)
                        sc_Follow(i.id)
                        x += 1
            elif x >= count:
                return


def sc_cleanFollowers():
    print('start sc_cleanFollowers')
    count = 0
    followers = sc_myFollowers()
    followings = sc_iFollow()
    for i in followings:
        print('Checking ' + client_xeno.get('/users/' + str(i)).username)
        if (i not in followers and client_xeno.get('/users/' + str(i)).followers_count < 9000) or (client_xeno.get('/users/' + str(i)).followers_count < 120):
            if count < 50:
                sc_Unfollow(i)
                print('Unfollowed ' + client_xeno.get('/users/' + str(i)).username)
                count+=1
            else:
                print('50 done')
                break
    print('cleanFollowers done')
    return



flag = open('f.txt', 'r')
f = flag.read(1)
flag.close()

fw = open('f.txt', 'w+')

if f == 'c':
    sc_cleanFollowers()
    mfc = client_xeno.get('me').followings_count
    if mfc <= 1700:
        fw.write('f sample text')
        print('Done')
    else:
        fw.write('c sample text')
        print('Done')
elif f == 'f':
    sc_FollowFollowers(251087)
    mfc = client_xeno.get('me').followings_count
    if mfc >= 1900:
        fw.write('c sample text')
        print('Done')
    else:
        fw.write('f sample text')
        print('Done')


fw.close()

add.close()
