#!/usr/bin/python3.6

import soundcloud as sc
import random

# Id of user which followers you would follow
reference_user_id = 1
token = 'access_token'
client = sc.Client(access_token=token)
me = client.get('me')

# Here you put comments you'd like to put on tracks while following
comments = []

with open('reject.txt', mode='r') as read:
    reject = list(map(int, read.read().split()))

add = open('reject.txt', mode='a')


def main_func():
    "Either start following or unfollowing process, depending on the flag value."
    with open('f.txt', 'r') as fr:
        f = fr.read(1)
    with open('f.txt', 'w+') as fw:
        mfc = me.followings_count
        if f == 'c':
            sc_cleanFollowers()
            if mfc <= 1700:
                fw.write('f sample text')
                print('Done')
            else:
                fw.write('c sample text')
                print('Done')
        elif f == 'f':
            sc_followFollowers(reference_user_id)
            if mfc >= 1900:
                fw.write('c sample text')
                print('Done')
            else:
                fw.write('f sample text')
                print('Done')
        else:
            fw.write('f sample text')
            print('Something got wrong...', f"\nF = {f}")
            

def sc_iFollow() -> list:
    "Get the list of user ids, that I follow."

    i_follow = client.get('/me/followings/', linked_partitioning=1, limit=200, order='id')
    out = [f.id for f in i_follow.collection]

    while i_follow.next_href != None:
        i_follow = client.get(i_follow.next_href, linked_partitioning=1, limit=200, order='id')
        out += [f.id for f in i_follow.collection]

    return out


def sc_myFollowers() -> list:
    "Get the list of user ids, that follow me."

    my_follow = client.get('/me/followers/', linked_partitioning=1, limit=200, order='id')
    out = [f.id for f in my_follow.collection]

    while my_follow.next_href != None:
        my_follow = client.get(my_follow.next_href, linked_partitioning=1, limit=200, order='id')
        out += [f.id for f in my_follow.collection]

    return out


def sc_iLike() -> list:
    "Get the list of user ids, that I like."
    i_like = client.get('/me/favorites/', linked_partitioning=1, limit=200, order='id')
    out = [f.id for f in i_like.collection]
    try:
        while i_like.next_href != None:
            i_like = client.get(i_like.next_href, linked_partitioning=1, limit=200, order='id')
            out += [f.id for f in i_like.collection]
    except AttributeError:
        pass
    return out


def sc_Like(id: int):
    "Add track in favorites, by track id."
    try:
        client.put('/me/favorites/' + str(id))
    except Exception as e:
        print(e)


def sc_postComment(id: int):
    "Post random comment on track, by track id."
    try:
        x = client.get('/tracks/{id}/'.format(id)).duration
        if int(me.id) != int(id):
            client.post('/tracks/{id}/comments'.format(id), comment={
                'body': comments.pop(random.choice(comments)),
                'timestamp': x/random.randint(2, 10)
            })
    except Exception as e:
        print(e)


def sc_Follow(id: int):
    "Follow user, by user id."
    try:
        client.put('/me/followings/{id}'.format(id))
    except Exception as e:
        print(e)


def sc_Unfollow(id: int):
    "Unfollow user, by user id."
    try:
        client.delete('/me/followings/{id}'.format(id))
        add.write(str(id) + ' ')
    except Exception as e:
        print(e)


def sc_followFollowers(id: int):
    "Follow users that follow some other person if they have enough followings as well, until count is not reached."
    print('Following...')
    i_f, count, reject_count, x, j = sc_iFollow(), 40 + random.randint(0,10), 120, 0, []
    new_follow = client.get(f'/users/{id}/followers/', limit=1, linked_partitioning=1)
    next_href = new_follow.next_href
    new_follow_next = client.get(next_href, limit=200, linked_partitioning=1)
    while new_follow_next.next_href != None:
        next_href = new_follow_next.next_href
        for i in new_follow_next.collection:
            if (((i.id not in i_f) and (x < count)) and ((i.id not in j) and (i.followers_count >= reject_count))) and (i.id not in reject):
                try:
                    t = client.get(f'/users/{i.id}/tracks/')[0].id
                    sc_Like(t)
                    sc_postComment(t)
                except:
                    pass
                print('Followed ' + i.username)
                j.append(i.id)
                sc_Follow(i.id)
                x += 1
            elif x >= count:
                print('Following done.')
                return
        del new_follow_next
        new_follow_next = client.get(next_href, limit=200, linked_partitioning=1)


def sc_cleanFollowers():
    "Clear space in followings."
    print('Unfollowing...')
    followers = sc_myFollowers()
    followings = sc_iFollow()
    low_edge, high_edge, unfollow_rate = 130, 9000, 50
    n = 0
    for i in followings:
        user = client.get(f'/users/{i}')
        print('Checking ' + user.username)
        if (i not in followers and user.followers_count < high_edge) or (user.followers_count < low_edge):
            if n < unfollow_rate:
                sc_Unfollow(i)
                n += 1
                print('Unfollowed ' + user.username)
            else:
                print('Unfollowing done.')
                return
    print('Adjust edges.')

if __name__ == '__main__':
    main_func()

add.close()
