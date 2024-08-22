#!/usr/bin/env python3

from config import app, db
from models import User, Product

with app.app_context():
    print('Deleting existing product...')
    

    print('Creating product objects...')
    lego_city_60373 = Product(
        name='LEGO City Fire Rescue Boat 60373',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h0d/h02/34463990448158.jpg",
        price="22.00",
        description="Exciting firefighting adventures await with this LEGO City Fire Rescue Boat (60373) playset, featuring a cool toy fireboat and speedboat dinghy. Kids can launch LEGO water elements from the boat’s extinguisher and firefighter jetpack to knock out the LEGO flames. Just add the 3 included minifigures and let the fun begin. Digital building fun for kids aged 5+",
        product_depth='6.1',
        product_weight='0.354',
        product_height='19.1',
        product_width='26.2',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=False,
        discount="0.00"
    )
    lego_city_60415 = Product(
        name='LEGO City Police Car and Muscle Car Chase 60415',
        image="https://www.bigw.com.au/medias/sys_master/images/images/heb/hed/47325768810526.jpg",
        price='22.00',
        description="Unleash high-speed fun and excitement with this police car toy playset for kids aged 6 and over. The LEGO City Police Car and Muscle Car Chase (60415) set for boys and girls features a cool police interceptor and a getaway vehicle, plus officer and crook minifigures for fun role play and storytelling.",
        product_depth='6.1',
        product_weight='0.354',
        product_height='19.1',
        product_width='26.2',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=False,
        discount="0.00"
    )
    lego_technic_42147 = Product(
        name='LEGO Technic Dump Truck 42147',
        image="https://www.bigw.com.au/medias/sys_master/images/images/hfd/h1f/34805061386270.jpg",
        price='14.00',
        description="Looking for a treat for building site fans? Kids aged 7 and over will love building and playing with this LEGO Technic Dump Truck (42147) toy set. It’s a great introduction to the world of LEGO Technic and helps young builders learn new engineering skills.",
        product_depth='6.1',
        product_weight='0.148',
        product_height='14.1',
        product_width='15.7',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=False,
        discount="0.00"
    )
    lego_technic_42166 = Product(
        name='LEGO Technic NEOM McLaren Extreme E Race Car 42166',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h29/h8a/47254566600734.jpg",
        price='35.00',
        description="Looking for an exciting gift for kids who love racing car toys? This pull-back car for boys and girls aged 7+ delivers thrills at every turn. First youngsters can enjoy building the LEGO® Technic NEOM McLaren Extreme E Race Car (42166).",
        product_depth='7.2',
        product_weight='0.407',
        product_height='14.1',
        product_width='26.2',
        is_it_new=True,
        is_it_clearance=False,
        is_it_onsale=False,
        discount="0.00"
    )
    barbie_self_care = Product(
        name='Barbie Self-Care Rise & Relax Doll',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h48/h04/32571164033054.jpg",
        price='37.00',
        description="Kids can practice mindfulness and meditate with the Barbie Rise and Relax doll to help feel relaxed during the day and to fall asleep at night! This fully posable doll has 6 different guided meditations with light, sound and soothing music across 2 different modes: Daytime and Night. ",
        product_depth='13.97',
        product_weight='0.349',
        product_height='21.59',
        product_width='7.5',
        is_it_new=True,
        is_it_clearance=False,
        is_it_onsale=False,
        discount="0.00"
    )
    barbie_doll_pool = Product(
        name='Barbie Doll and Pool Playset',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h94/h26/47144430403614.jpg",
        price='19.00',
        description="Slide into summer fun with Barbie doll and her pool! It's easy to fill and empty for an instant pool party. Help Barbie climb the ladder and go down the slide, then relax in the water with a refreshing drink!",
        product_depth='27.0',
        product_weight='0.6',
        product_height='15.0',
        product_width='39.0',
        is_it_new=True,
        is_it_clearance=False,
        is_it_onsale=False,
        discount="0.00"
    )
    minecraft_blaster = Product(
        name='Nerf Minecraft Heartstealer Dart Blaster',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h86/h36/34532588650526.jpg",
        price='25.00',
        description="These huggable 8 and 12 PAW Patrol plush feature everyone's favorite rescue dogs in their classic uniforms with adorable minimalist designs and accurate details from the cartoon.",
        product_depth='6.6',
        product_weight='0.544',
        product_height='19.0',
        product_width='27.9',
        is_it_new=False,
        is_it_clearance=True,
        is_it_onsale=False,
        discount="20.00"
    )
    paw_patrol_plush = Product(
        name='Paw Patrol Trend 30cm Plush - Skye"',
        image="https://www.bigw.com.au/medias/sys_master/images/images/hd3/h84/45034866409502.jpg",
        price='19.00',
        description="The PAW pups are here in a fun, super-squishy new shape! Bring home your favorite cuddly PAW Patrol pup for playtime rescue missions at home, now in a squishier format than ever!",
        product_depth='19.7',
        product_weight='0.14',
        product_height='30.0',
        product_width='25.4',
        is_it_new=False,
        is_it_clearance=True,
        is_it_onsale=False,
        discount="5.00"
    )
    gabby_dollhouse = Product(
        name="Gabby's Dollhouse Monopoly Jr",
        image="https://www.bigw.com.au/medias/sys_master/images/images/h0f/h93/45509950570526.jpg",
        price='17.00',
        description="Visit Gabby's Dollhouse in this a-meow-zing edition of MONOPOLY Junior! Jump around the game board visiting the Gabby Cats and exploring their rooms, from Cakey's Kitchen to DJ's Music Room. Land on CatRat, Kitty Fairy and Pandy Paws! ",
        product_depth='0.8',
        product_weight='0.36',
        product_height='30.00',
        product_width='25.4',
        is_it_new=False,
        is_it_clearance=True,
        is_it_onsale=False,
        discount="12.00"
    )
    one_trick_pony = Product(
        name='One Trick Pony',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h85/h88/35120009084958.jpg",
        price='18.00',
        description="Howdy partner! This cowboy is keepin' a watchful eye over his farm and isn't afraid to hogtie any varmint who tries to mess with his herd. His lasso is fast, so step lively! Take turns trying to sneak his animals across the fence - but don't get caught!",
        product_depth='2.1',
        product_weight='0.345',
        product_height='17.1',
        product_width='9.6',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=True,
        discount="7.00"
    )
    happy_kid_blaster = Product(
        name='Happy Kid Space Blaster',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h27/h46/10824491958302.jpg",
        price='8.00',
        description="Be battle-prepared with the Space Blaster from Happy Kid. Featuring a light up blade, laser booster, ergonomic handle and the option to convert between pistol and sword mode, this Space Blaster is a must-have in your arsenal!",
        product_depth='3.1',
        product_weight='0.25',
        product_height='14.5',
        product_width='6.7',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=True,
        discount="3.50"
    )
    grafix_game = Product(
        name='Grafix Dinosaur Operation Game',
        image="https://www.bigw.com.au/medias/sys_master/images/images/hc0/hee/11843586195486.jpg",
        price='8.85',
        description="Keep your hands steady to avoid having a shocker in the Dinosaur Operation Game.Grab the most body parts and get the most points to win! A great game for 2-4 players. Please note: 2 x AA batteries are required (not included).",
        product_depth='2.1',
        product_weight='0.23',
        product_height='16.4',
        product_width='14.1',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=True,
        discount="4.15"
    )
    sonic_action_deluxe = Product(
        name="Sonic Prime Action Figures 6 Pack Deluxe Box - Assorted*",
        image="https://www.bigw.com.au/medias/sys_master/images/images/h79/h4e/48190958927902.jpg",
        price='39.00',
        description="Collect all 8 officially licensed Sonic Prime figures, based off your favourite characters from the record breaking Netflix show. Each Deluxe Box contains 6 x 7.5cm figures, each sitting on a black play or display base. Collect Sonic, Tails, Amy Rose, Doctor Eggman, and more!",
        product_depth='1.3',
        product_weight='0.32',
        product_height='4.5',
        product_width='6.7',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=False,
        discount="0.00"
    )
    money_around = Product(
        name='Monkey Around',
        image="https://www.bigw.com.au/medias/sys_master/images/images/hf2/hcd/48292966957086.jpg",
        price='29.00',
        description="The Wiggle & Giggle Game prompting players to do simple movements such as balancing, hopping and marching together. Parent guide included. Kids learn hand-eye coordination, imitation, and gross motor-skills while building their vocabulary!",
        product_depth='3.5',
        product_weight='0.42',
        product_height='8.3',
        product_width='8.3',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=False,
        discount='0.00'
    )
    hard_quiz_game = Product(
        name='Hard Quiz Fast Game',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h8a/h90/48343706173470.jpg",
        price='19.00',
        description="Play Hard Quiz - Hard and Fast! Just like the popular TV Quiz Show you can play an Expert Round, Tom's Round and People's Round. Are you buzzing for bees? Or passionate for punk rock? Find out could win Hard Quiz, at home. Age 13+",
        product_depth='3.2',
        product_weight='0.5',
        product_height='12.2',
        product_width='6.0',
        is_it_new=True,
        is_it_clearance=False,
        is_it_onsale=False,
        discount='0.00'
    )
    pokemon_blister_pack = Product(
        name="Pokemon TCG: Scarlet & Violet - Temporal Forces Blister Pack - Assorted*",
        image="https://www.bigw.com.au/medias/sys_master/images/images/h05/h50/48159836143646.jpg",
        price='7.00',
        description="The ranks of Ancient and Future Pokémon continue to grow! Walking Wake ex breaks free of the past alongside Raging Bolt ex, while Iron Leaves ex delivers high-tech justice with Iron Crown ex",
        product_depth='0.1',
        product_weight='0.04',
        product_height='6.8',
        product_width='4.5',
        is_it_new=True,
        is_it_clearance=False,
        is_it_onsale=False,
        discount='0.00'
    )
    petshop_farm = Product(
        name='Littlest Pet Shop Farm Besties Collector 5 Pack"',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h00/hfb/48556160090142.jpg",
        price='35.00',
        description="Calling all new and original Littlest Pet Shop fans! LPS Generation 7 has arrived. Collect a new generation of bobblin' head pets with over 65 exciting new friends in series 1. Panda, cat, axolotl, anteater and so many more are eager to become your new besties!",
        product_depth='3.1',
        product_weight='0.8',
        product_height='13.1',
        product_width='8.5',
        is_it_new=False,
        is_it_clearance=True,
        is_it_onsale=False,
        discount='15.00'
    )
    rusco_racing = Product(
        name='Rusco Racing 1:10 Dirt Maxx Motorbike',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h17/hf2/34653044244510.jpg",
        price='89.00',
        description="1:10 Scale so super large motorbike and full suspension system for easy riding",
        product_depth='4.3',
        product_weight='1.2',
        product_height='21.2',
        product_width='14.5',
        is_it_new=False,
        is_it_clearance=True,
        is_it_onsale=False,
        discount='20.00'
    )
    hotwheel_raceoff = Product(
        name='Hot Wheels Multi-Loop Raceoff',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h36/h39/31673417859102.jpg",
        price='39.00',
        description="For exciting racing that's downright loopy, the Hot Wheels Multi-Loop Race Off Playset delivers! Race down the track through a series of loops to score points and be the first through the massive loop, busting it open and leaving the competition in the dust.",
        product_depth='5.6',
        product_weight='2.1',
        product_height='11.2',
        product_width='20.2',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=True,
        discount='10.00'
    )
    minecraft_alex = Product(
        name='Minecraft Make Your Own Alex',
        image="https://www.bigw.com.au/medias/sys_master/images/images/h17/hd9/47968219037726.jpg",
        price='19.00',
        description="Make Your Own Minecraft Alex from sustainable materials! Once the easy to assemble cardboard kits are complete, you can pose Alex and add accessories like pickaxes and helmets!",
        product_depth='6.7',
        product_weight='1.4',
        product_height='23.5',
        product_width='14.5',
        is_it_new=False,
        is_it_clearance=False,
        is_it_onsale=True,
        discount='5.00'
    )

    print('Adding product object to transaction... ')
    db.session.add_all([lego_city_60373,lego_city_60415,lego_technic_42147,lego_technic_42166,
    barbie_self_care,barbie_doll_pool,minecraft_blaster,paw_patrol_plush,gabby_dollhouse,one_trick_pony,happy_kid_blaster,
    grafix_game,sonic_action_deluxe,money_around,hard_quiz_game,pokemon_blister_pack,petshop_farm,rusco_racing,
    hotwheel_raceoff,minecraft_alex])
    # db.session.add_all([lego_city_60373, lego_city_60415])

    print('Committing transaction...')
    db.session.commit()

    print('Complete.')