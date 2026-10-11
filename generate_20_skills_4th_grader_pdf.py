# -*- coding: utf-8 -*-
"""
generate_20_skills_4th_grader_pdf.py
Polish & typography overhaul:
1. Strips raw unicode emojis from standard PDF fonts (which render as black boxes) and replaces them with crisp, clean vector badge icons and symbols.
2. Proper proportional word wrapping for One-Liner box and Title bar (no clipped words).
3. Rich visual diagrams: Custom vector graphics for each skill type with colorful nodes, connecting wires, checkmarks, padlocks, and badges!
4. Clear 4th-grader tone across all 20 pages.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

PDF_FILENAME = "20_Agentic_Skills_Explained_For_4th_Graders.pdf"

SKILLS_DATA = [
    # ==========================================
    # TIER 0: PHYSICAL CLOUD HARDWARE (Pages 1 - 7)
    # ==========================================
    {
        "page": 1,
        "id": "aws-bedrock",
        "title": "Amazon Bedrock: The Idea Machine",
        "tier": "Tier 0: Cloud Hardware",
        "tier_color": colors.HexColor("#059669"),
        "hero_name": "Buzzy the Idea Robot",
        "symbol": "IDEA",
        "badge_bg": colors.HexColor("#d1fae5"),
        "badge_fg": colors.HexColor("#065f46"),
        "accent": colors.HexColor("#10b981"),
        "one_liner": "A super-fast imagination machine that comes up with cool ideas, but isn't allowed to touch anything in real life!",
        "story": (
            "Imagine you have a robot friend named Buzzy who is amazing at writing mystery stories and dreaming up giant LEGO castles. "
            "Whenever you ask him a question, Buzzy writes down a blueprint on a piece of paper. But here is the secret rule: "
            "Buzzy has NO hands! He is only allowed to suggest ideas. He cannot touch the scissors, paint the walls, or spend real coins. "
            "He just says: 'Hey, what if we built this castle?' and hands you the drawing!"
        ),
        "diagram_type": "idea_box",
        "diagram_caption": "Buzzy writes an idea on paper  -->  Hands are locked safely away from real toys!",
        "superpower": "Super-fast brainstorming without any risk of breaking real toys!",
        "kid_rule": "The Idea Maker proposes, but never pushes the real button!"
    },
    {
        "page": 2,
        "id": "aws-agentcore",
        "title": "AgentCore: The Hallway Hall Monitor",
        "tier": "Tier 0: Cloud Hardware",
        "tier_color": colors.HexColor("#059669"),
        "hero_name": "Officer Cedar the Hall Monitor",
        "symbol": "SHIELD",
        "badge_bg": colors.HexColor("#d1fae5"),
        "badge_fg": colors.HexColor("#065f46"),
        "accent": colors.HexColor("#059669"),
        "one_liner": "The strict playground security guard who checks your hall pass before you can enter the room!",
        "story": (
            "Remember that strict hall monitor who stands outside the principal's office? Even if you run up shouting 'I have an emergency!', "
            "Officer Cedar stops you, puts his hand out, and asks: 'Do you have a signed hall pass?' "
            "AgentCore is that exact guard for computers. When an AI bot wants to delete a file or move money, AgentCore pulls out his rulebook. "
            "If the pass says NO, the door stays locked tight. No exceptions, not even for smart robots!"
        ),
        "diagram_type": "guard_gate",
        "diagram_caption": "Robot asks to enter  -->  Officer Cedar checks hall pass  -->  PASS or NO ENTRY!",
        "superpower": "Blocks unauthorized moves before anything bad can happen!",
        "kid_rule": "No hall pass? No entry. Zero rule breaking allowed!"
    },
    {
        "page": 3,
        "id": "aws-s3-vault",
        "title": "Amazon S3 Vault: The Time Capsule",
        "tier": "Tier 0: Cloud Hardware",
        "tier_color": colors.HexColor("#059669"),
        "hero_name": "The Golden Fortress Safe",
        "symbol": "VAULT",
        "badge_bg": colors.HexColor("#d1fae5"),
        "badge_fg": colors.HexColor("#065f46"),
        "accent": colors.HexColor("#0d9488"),
        "one_liner": "A magical metal safe where once you drop a diary page in, nobody on earth can ever erase it!",
        "story": (
            "Have you ever made a promise and wished you could carve it in solid diamond so no one could ever lie about it later? "
            "That is S3 WORM Vault! When an AI finishes a test or scores a soccer goal, it writes down the receipt and drops it through "
            "a one-way mail slot into a titanium safe. The lock is frozen for 7 whole years. Even the principal and computer boss cannot "
            "erase it or scribble over it. It proves exactly what happened!"
        ),
        "diagram_type": "time_capsule",
        "diagram_caption": "Diary note dropped inside  -->  Locked with giant padlock for 7 years!",
        "superpower": "Guarantees 100% honesty because you cannot change history!",
        "kid_rule": "Once it is dropped inside the safe, it stays forever!"
    },
    {
        "page": 4,
        "id": "aws-database",
        "title": "AWS Database: The Super-Locker",
        "tier": "Tier 0: Cloud Hardware",
        "tier_color": colors.HexColor("#059669"),
        "hero_name": "Locker-Bot with 3 Secret Drawers",
        "symbol": "LOCKER",
        "badge_bg": colors.HexColor("#d1fae5"),
        "badge_fg": colors.HexColor("#065f46"),
        "accent": colors.HexColor("#0284c7"),
        "one_liner": "A super-smart locker that holds keys, detective maps, and memory drawers so toys don't get mixed up!",
        "story": (
            "Imagine your school locker has 3 magic drawers. Drawer #1 has a special key card: whoever grabs it gets to play with the soccer ball, "
            "and nobody else can touch it until it is returned. Drawer #2 has a magnifying glass that finds all your matching baseball cards in 1 second. "
            "Drawer #3 has a spiderweb map connecting all your best friends. This locker keeps millions of toys organized without any fighting!"
        ),
        "diagram_type": "triple_drawer",
        "diagram_caption": "Drawer 1: Soccer Ball Key  |  Drawer 2: Card Matcher  |  Drawer 3: Friendship Map",
        "superpower": "Instantly remembers facts and stops two kids from fighting over the same toy!",
        "kid_rule": "One key per kid at a time = zero arguments!"
    },
    {
        "page": 5,
        "id": "aws-lambda",
        "title": "AWS Lambda: The Pop-Up Tent",
        "tier": "Tier 0: Cloud Hardware",
        "tier_color": colors.HexColor("#059669"),
        "hero_name": "The 10-Second Pop-Up Tent",
        "symbol": "SANDBOX",
        "badge_bg": colors.HexColor("#d1fae5"),
        "badge_fg": colors.HexColor("#065f46"),
        "accent": colors.HexColor("#ea580c"),
        "one_liner": "A temporary play-tent that pops up in 1 second to do your math homework, then disappears completely!",
        "story": (
            "What if you had a pop-up tent that you threw on the grass whenever you had math homework? You hop inside, use the calculator, "
            "solve 50 fractions in 2 seconds, and then *POOF!* The tent folds itself up and vanishes into thin air. "
            "Because the tent disappears every single time, it is always sparkling clean. No messy crumbs or viruses from yesterday's homework "
            "can ever spill into today's assignment!"
        ),
        "diagram_type": "popup_tent",
        "diagram_caption": "Poof! Tent appears  -->  Math done in 2 sec  -->  Poof! Tent disappears clean!",
        "superpower": "Fresh, clean sandbox workspace every single time with zero mess left behind!",
        "kid_rule": "Do the math, pack up the tent, leave no mess!"
    },
    {
        "page": 6,
        "id": "aws-stepfunctions",
        "title": "AWS Step Functions: The Board Game Referee",
        "tier": "Tier 0: Cloud Hardware",
        "tier_color": colors.HexColor("#059669"),
        "hero_name": "The Hopscotch Referee",
        "symbol": "STEPS",
        "badge_bg": colors.HexColor("#d1fae5"),
        "badge_fg": colors.HexColor("#065f46"),
        "accent": colors.HexColor("#4f46e5"),
        "one_liner": "A board game referee who makes sure you hop on Step 1, then Step 2, and never skip ahead to Step 5!",
        "story": (
            "Playing Candy Land or Hopscotch is only fun when everyone follows the steps in order. Step Functions is the master referee. "
            "It holds a checklist: 'Step 1: Wash hands. Step 2: Eat lunch. Step 3: Brush teeth.' If you try to brush your teeth before washing "
            "your hands, the referee blows his whistle: *TWEET!* 'Go back to Step 1!' And if you drop your ice cream, the referee safely rolls you "
            "back to start so nobody gets hurt."
        ),
        "diagram_type": "hopscotch",
        "diagram_caption": "Box 1  -->  Box 2  -->  Box 3  -->  If mistake happens, slide safely back to start!",
        "superpower": "Guarantees you never skip a step or lose your place in a recipe!",
        "kid_rule": "Step 1 before Step 2, every single time!"
    },
    {
        "page": 7,
        "id": "aws-client-api",
        "title": "AWS EventBridge: The Walkie-Talkie Network",
        "tier": "Tier 0: Cloud Hardware",
        "tier_color": colors.HexColor("#059669"),
        "hero_name": "Walkie-Talkie Dispatcher",
        "symbol": "RADIO",
        "badge_bg": colors.HexColor("#d1fae5"),
        "badge_fg": colors.HexColor("#065f46"),
        "accent": colors.HexColor("#e11d48"),
        "one_liner": "A high-speed walkie-talkie network that delivers secret messages across the entire school playground!",
        "story": (
            "Imagine you are on the swings and your friend is way over on the soccer field. How do you tell them recess is ending in 5 minutes? "
            "You use the playground walkie-talkie! EventBridge listens for news: 'Attention, lunch is ready!' or 'Recess is over!' "
            "It instantly zips that message to only the kids who need to hear it, without screaming on the loudspeaker and waking up the kindergarten nap room."
        ),
        "diagram_type": "walkie_talkie",
        "diagram_caption": "Walkie-Talkie Beeps  -->  Sends message only to the right teammate!",
        "superpower": "Delivers the right message to the right robot without shouting!",
        "kid_rule": "Whisper to your friends, don't scream on the loudspeaker!"
    },

    # ==========================================
    # TIER 1: AGENT OS KERNEL (Pages 8 - 14)
    # ==========================================
    {
        "page": 8,
        "id": "kernel-propose-decide",
        "title": "Kernel Propose-Decide: The Grown-Up Brain Filter",
        "tier": "Tier 1: Robot Brain OS",
        "tier_color": colors.HexColor("#2563eb"),
        "hero_name": "The Prefrontal Brain Judge",
        "symbol": "JUDGE",
        "badge_bg": colors.HexColor("#dbeafe"),
        "badge_fg": colors.HexColor("#1e40af"),
        "accent": colors.HexColor("#2563eb"),
        "one_liner": "Your inner coach that stops you from yelling silly things and makes sure you only do smart moves!",
        "story": (
            "Have you ever had a silly thought like: 'What if I jump off the couch wearing cardboard wings?' That silly thought came from "
            "your wild imagination (Ring 3). But before your legs jumped, your grown-up inner judge (Ring 0) chimed in: 'Wait, that will hurt! Let us build a pillow fort instead.' "
            "That is what Propose-Decide does: the AI model dreams up 100 wild ideas, but the Brain Judge approves only the safe ones!"
        ),
        "diagram_type": "brain_filter",
        "diagram_caption": "Wild Idea: 'Jump off couch!'  -->  Brain Filter: 'DENIED! Build pillow fort!'",
        "superpower": "Filters out silly impulses so the robot never does something dangerous!",
        "kid_rule": "Think before you jump!"
    },
    {
        "page": 9,
        "id": "kernel-runbook-engine",
        "title": "Kernel Runbook: The LEGO Assembly Guide",
        "tier": "Tier 1: Robot Brain OS",
        "tier_color": colors.HexColor("#2563eb"),
        "hero_name": "The Master Builder Guide",
        "symbol": "MANUAL",
        "badge_bg": colors.HexColor("#dbeafe"),
        "badge_fg": colors.HexColor("#1e40af"),
        "accent": colors.HexColor("#3b82f6"),
        "one_liner": "A colorful step-by-step LEGO instruction booklet that shows you which brick to snap on next!",
        "story": (
            "When you open a giant Millennium Falcon LEGO box with 2,000 pieces, you don't just dump all the pieces on the rug and guess. "
            "You open Book 1, Page 1! You snap the yellow brick to the blue brick. Once that page is done, you turn to Page 2. "
            "The Runbook Engine gives the AI robot that exact instruction booklet. It won't let the robot start building the spaceship roof "
            "until the foundation bricks are clicked in tight!"
        ),
        "diagram_type": "lego_manual",
        "diagram_caption": "Step 1: Base Bricks  -->  Step 2: Wheels  -->  Step 3: Wings! No skipping!",
        "superpower": "Turns giant complicated missions into simple, foolproof steps!",
        "kid_rule": "Follow the booklet step-by-step to build a masterpiece!"
    },
    {
        "page": 10,
        "id": "kernel-supervisor-circuit",
        "title": "Kernel Supervisor: The Watchdog Sparky",
        "tier": "Tier 1: Robot Brain OS",
        "tier_color": colors.HexColor("#2563eb"),
        "hero_name": "Watchdog Sparky",
        "symbol": "WATCHDOG",
        "badge_bg": colors.HexColor("#dbeafe"),
        "badge_fg": colors.HexColor("#1e40af"),
        "accent": colors.HexColor("#ef4444"),
        "one_liner": "A friendly watchdog who taps the robot on the shoulder if it gets stuck running in circles!",
        "story": (
            "Have you ever seen a dog chase its own tail around and around in a dizzy circle? If nobody stops him, he will fall over! "
            "Sometimes, an AI gets stuck saying: 'Uh, what was I doing? Uh, what was I doing?' over and over again. "
            "Watchdog Sparky watches the clock with an egg timer. If the robot spins in circles 3 times or burns through too much energy, "
            "Sparky barks *WOOF!*, pulls the safety lever, and says: 'Time out! Take a nap and reset!'"
        ),
        "diagram_type": "watchdog_timer",
        "diagram_caption": "Robot dizzy in circles  -->  Watchdog rings bell: DING!  -->  Robot resets safely!",
        "superpower": "Stops runaway loops and keeps battery energy from being wasted!",
        "kid_rule": "If you are dizzy, stop and take a breath!"
    },
    {
        "page": 11,
        "id": "kernel-mutex-lease",
        "title": "Kernel Mutex: The Magic Talking Stick",
        "tier": "Tier 1: Robot Brain OS",
        "tier_color": colors.HexColor("#2563eb"),
        "hero_name": "The Talking Stick Keeper",
        "symbol": "STICK",
        "badge_bg": colors.HexColor("#dbeafe"),
        "badge_fg": colors.HexColor("#1e40af"),
        "accent": colors.HexColor("#8b5cf6"),
        "one_liner": "In circle time, only the kid holding the magic stick is allowed to speak, so nobody talks at the same time!",
        "story": (
            "In Kindergarten circle time, what happens if all 25 kids try to tell their show-and-tell stories at the exact same second? "
            "Total noisy chaos! Nobody can hear a word! That is why teacher gives out the Talking Stick. Whoever holds the wooden stick gets "
            "to talk for 15 seconds. When their turn is over, they hand it to the next kid. "
            "The Mutex Lease does that for computer records so two robots never write on the same paper at once!"
        ),
        "diagram_type": "talking_stick",
        "diagram_caption": "Kid with Talking Stick = TALKS  |  Other kids = LISTEN & WAIT TURN!",
        "superpower": "Eliminates noisy collisions and accidental overwrites forever!",
        "kid_rule": "Wait for the stick before you take your turn!"
    },
    {
        "page": 12,
        "id": "kernel-context-pager",
        "title": "Kernel Context Pager: The Pocket Backpack",
        "tier": "Tier 1: Robot Brain OS",
        "tier_color": colors.HexColor("#2563eb"),
        "hero_name": "Pocket Backpack Organizer",
        "symbol": "POCKET",
        "badge_bg": colors.HexColor("#dbeafe"),
        "badge_fg": colors.HexColor("#1e40af"),
        "accent": colors.HexColor("#06b6d4"),
        "one_liner": "A magic backpack that keeps only 3 colored pencils in your hands, and packs older markers into the closet!",
        "story": (
            "If you tried to carry 50 textbooks, 200 crayons, and 5 water bottles in your hands all at once while walking to class, "
            "you would drop everything on the floor! An AI robot's short-term brain can only hold a few thoughts at a time. "
            "The Context Pager is a pocket organizer: it keeps the pencil you need right now in your shirt pocket, and neatly packs "
            "last week's history homework into the classroom closet. When you need it again, it swaps them in a snap!"
        ),
        "diagram_type": "pocket_swap",
        "diagram_caption": "Shirt Pocket: 3 active pencils  |  Closet: 50 archived markers!",
        "superpower": "Keeps your working hands light and sharp with zero memory clutter!",
        "kid_rule": "Keep only what you need right now in your hands!"
    },
    {
        "page": 13,
        "id": "kernel-episodic-ledger",
        "title": "Kernel Episodic Ledger: The Wax Stamp Diary",
        "tier": "Tier 1: Robot Brain OS",
        "tier_color": colors.HexColor("#2563eb"),
        "hero_name": "The Unbreakable Stamp Diary",
        "symbol": "STAMP",
        "badge_bg": colors.HexColor("#dbeafe"),
        "badge_fg": colors.HexColor("#1e40af"),
        "accent": colors.HexColor("#6366f1"),
        "one_liner": "A diary where every page has a secret wax stamp matching the page before it, so no pages can be torn out!",
        "story": (
            "Imagine you have a private detective diary. Every day after solving a case, you stamp Page 1 with red wax. "
            "On Page 2, you melt the wax from Page 1 into the new seal. This creates an unbreakable chain of stamps: Page 1  -->  Page 2  -->  Page 3. "
            "If a sneaky villain tried to rip out Page 2 or change the clues, the wax seal on Page 3 would instantly crack and tell everyone! "
            "This gives the robot a flawless, tamper-proof memory of everything it did!"
        ),
        "diagram_type": "wax_chain",
        "diagram_caption": "Page 1 Seal  -->  melted into Page 2  -->  melted into Page 3! Unbreakable chain!",
        "superpower": "Makes it impossible for anyone to secretly alter past memories!",
        "kid_rule": "A chain of wax stamps keeps the truth safe!"
    },
    {
        "page": 14,
        "id": "kernel-grounding-certifier",
        "title": "Kernel Grounding: The 3-Friend Fact Checker",
        "tier": "Tier 1: Robot Brain OS",
        "tier_color": colors.HexColor("#2563eb"),
        "hero_name": "Detective Triangulator",
        "symbol": "CLUES",
        "badge_bg": colors.HexColor("#dbeafe"),
        "badge_fg": colors.HexColor("#1e40af"),
        "accent": colors.HexColor("#0284c7"),
        "one_liner": "A detective who won't believe a rumor until three different best friends confirm it is 100% true!",
        "story": (
            "If someone on the playground tells you: 'Did you hear? Elephants learned how to fly!', do you instantly believe them? No way! "
            "You ask for proof! You check Friend #1 (Did you see a photo?), Friend #2 (Did the science teacher say so?), and Friend #3 (Is it written in the encyclopedia?). "
            "Only when all 3 friends agree does Detective Triangulator say: 'Okay, that is certified TRUE.' "
            "This stops the AI from hallucinating or making up imaginary stories!"
        ),
        "diagram_type": "three_detectives",
        "diagram_caption": "Check 1: Photo? YES  |  Check 2: Teacher? YES  |  Check 3: Book? YES = TRUE!",
        "superpower": "Crushes hallucinations by demanding 3 pieces of real proof!",
        "kid_rule": "Never believe a rumor without checking 3 facts!"
    },

    # ==========================================
    # TIER 2: MULTI-AGENT SWARMS (Pages 15 - 20)
    # ==========================================
    {
        "page": 15,
        "id": "swarm-topology-builder",
        "title": "Swarm Topology: The Shortcut Map",
        "tier": "Tier 2: Multi-Agent Swarm",
        "tier_color": colors.HexColor("#7c3aed"),
        "hero_name": "The Playground Secret Shortcut Map",
        "symbol": "MAP",
        "badge_bg": colors.HexColor("#ede9fe"),
        "badge_fg": colors.HexColor("#5b21b6"),
        "accent": colors.HexColor("#7c3aed"),
        "one_liner": "A clever clubhouse seating chart where everyone has buddies nearby, plus secret zip-lines across the yard!",
        "story": (
            "If 12 kids are playing across a huge 3-acre playground, how do you keep them connected without everyone screaming? "
            "You split them into 3 cool clubhouses: the Art Team, the Sports Team, and the Science Team. "
            "Kids in the same clubhouse sit in a close circle so they can whisper easily. Then, you build a secret zip-line shortcut "
            "between each clubhouse! Now, any kid on the playground can reach any other kid in just 2 quick hops!"
        ),
        "diagram_type": "clubhouse_shortcuts",
        "diagram_caption": "Clubhouse A  ==== Zip-Line ====  Clubhouse B  ==== Zip-Line ====  Clubhouse C",
        "superpower": "Connects big teams with short travel distance and zero screaming!",
        "kid_rule": "Sit with your buddies, but keep a zip-line to other clubs!"
    },
    {
        "page": 16,
        "id": "swarm-liaison-router",
        "title": "Swarm Liaison Router: The Classroom Ambassadors",
        "tier": "Tier 2: Multi-Agent Swarm",
        "tier_color": colors.HexColor("#7c3aed"),
        "hero_name": "Ambassador Leo",
        "symbol": "AMBASSADOR",
        "badge_bg": colors.HexColor("#ede9fe"),
        "badge_fg": colors.HexColor("#5b21b6"),
        "accent": colors.HexColor("#9333ea"),
        "one_liner": "The class captain chosen to deliver polite notes between Room 4A and Room 4B without causing a stampede!",
        "story": (
            "Imagine Mrs. Smith's class wants to challenge Mr. Johnson's class to a kickball game. "
            "Should all 30 students run down the hallway at once and barge into Room 4B? No, that would cause a stampede! "
            "Instead, the class picks Ambassador Leo. Leo walks politely down the hall, hands the challenge envelope to Room 4B's captain, "
            "and brings back the answer. That is the Liaison Router: one trusted messenger per pod keeps the school quiet and organized!"
        ),
        "diagram_type": "ambassador_bridge",
        "diagram_caption": "Room 4A  -->  Ambassador Leo walks note down hall  -->  Room 4B receives politely!",
        "superpower": "Prevents noisy hallway stampedes by sending one smart messenger!",
        "kid_rule": "Send one ambassador instead of the whole mob!"
    },
    {
        "page": 17,
        "id": "swarm-hop-limiter",
        "title": "Swarm Hop Limiter: The 3-Ticket Relay Rule",
        "tier": "Tier 2: Multi-Agent Swarm",
        "tier_color": colors.HexColor("#7c3aed"),
        "hero_name": "The Hot Potato Referee",
        "symbol": "TICKETS",
        "badge_bg": colors.HexColor("#ede9fe"),
        "badge_fg": colors.HexColor("#5b21b6"),
        "accent": colors.HexColor("#c026d3"),
        "one_liner": "A hot-potato referee who pops the balloon if kids keep passing it in circles without doing any work!",
        "story": (
            "Have you ever played Telephone, where a rumor gets passed from kid to kid until it turns into total gibberish? "
            "Or hot potato where kids just pass back and forth forever? "
            "The Hop Limiter stamps every message with 3 tickets. Pass 1: Ticket #1 used. Pass 2: Ticket #2 used. Pass 3: Last ticket! "
            "If someone tries to pass it a 4th time, the referee shouts: 'Out of tickets! You must finish the job right now!' "
            "This stops messages from getting lost in endless games of tag!"
        ),
        "diagram_type": "three_tickets",
        "diagram_caption": "Ticket 1 (used)  -->  Ticket 2 (used)  -->  Ticket 3 (used)  -->  WORK MUST BE DONE!",
        "superpower": "Kills endless games of tag so tasks actually get finished!",
        "kid_rule": "3 passes maximum, then you must score the goal!"
    },
    {
        "page": 18,
        "id": "swarm-shared-whiteboard",
        "title": "Swarm Whiteboard: The Giant Chalkboard",
        "tier": "Tier 2: Multi-Agent Swarm",
        "tier_color": colors.HexColor("#7c3aed"),
        "hero_name": "The 3-Column Chalkboard",
        "symbol": "BOARD",
        "badge_bg": colors.HexColor("#ede9fe"),
        "badge_fg": colors.HexColor("#5b21b6"),
        "accent": colors.HexColor("#4338ca"),
        "one_liner": "A big chalkboard at the front of the room divided into 3 neat columns so everyone sees the score without asking!",
        "story": (
            "Instead of 12 kids writing separate paper notes and throwing them at each other across the classroom, what is much smarter? "
            "Draw 3 big columns on the front chalkboard! "
            "Column 1 is for the Money Team. Column 2 is for the Rules Team. Column 3 is for the Builders Team. "
            "When the Builders want to know if they have enough wood, they don't whisper to 10 people—they just glance at Column 1 on the board! "
            "Everyone sees the exact same truth in 1 second!"
        ),
        "diagram_type": "three_columns",
        "diagram_caption": "[ Column 1: Money ]  |  [ Column 2: Rules ]  |  [ Column 3: Builders ]",
        "superpower": "Everyone stays on the same page without sending 100 confusing emails!",
        "kid_rule": "Put the score on the board so everyone knows what's happening!"
    },
    {
        "page": 19,
        "id": "swarm-consensus-arbiter",
        "title": "Swarm Byzantine Quorum: The Super-Vote",
        "tier": "Tier 2: Multi-Agent Swarm",
        "tier_color": colors.HexColor("#7c3aed"),
        "hero_name": "The Super-Vote Ballot Box",
        "symbol": "QUORUM",
        "badge_bg": colors.HexColor("#ede9fe"),
        "badge_fg": colors.HexColor("#5b21b6"),
        "accent": colors.HexColor("#7e22ce"),
        "one_liner": "A supermajority vote where at least 10 out of 12 teammates must raise their hands before picking the game!",
        "story": (
            "Imagine your 12-person kickball team is deciding whether to play on Field A or Field B. "
            "What if 2 kids are being silly or got tricked by the opposing team? If you needed all 12 kids to agree, 1 grumpy kid could freeze the whole game! "
            "The Byzantine Quorum uses the supermajority rule: as long as at least 10 out of 12 kids (more than two-thirds!) raise their hands and sign their ballots, "
            "the game starts! Even if 2 robots are glitching or grumpy, the team keeps winning!"
        ),
        "diagram_type": "quorum_hands",
        "diagram_caption": "10 Hands Raised (YES!) vs 2 Grumpy Kids (NO)  -->  SUPERMAJORITY WINS!",
        "superpower": "Makes fair, unstoppable decisions even if a few robots glitch out!",
        "kid_rule": "10 out of 12 agree = game on, no stalling allowed!"
    },
    {
        "page": 20,
        "id": "swarm-circuit-breaker",
        "title": "Swarm Circuit Breaker: The Red Card Whistle",
        "tier": "Tier 2: Multi-Agent Swarm",
        "tier_color": colors.HexColor("#7c3aed"),
        "hero_name": "Referee Whistle & Red Card",
        "symbol": "RED CARD",
        "badge_bg": colors.HexColor("#ede9fe"),
        "badge_fg": colors.HexColor("#5b21b6"),
        "accent": colors.HexColor("#be123c"),
        "one_liner": "A safety whistle that benches a runaway robot for 5 minutes so it doesn't bump into all its teammates!",
        "story": (
            "In soccer, what happens if one player loses their shoes, gets super dizzy, and starts kicking the ball into their own team's net? "
            "The referee blows the whistle: *TWEET!* 'Red card! Sit on the bench for 5 minutes and drink some cold water.' "
            "The Circuit Breaker is that referee whistle for multi-agent swarms. If an agent starts hallucinating or repeating itself, "
            "the circuit flips OPEN. Its lock is taken away and its teammates keep playing safely without it until it cools down!"
        ),
        "diagram_type": "red_card",
        "diagram_caption": "Glitching Robot  -->  Referee blows whistle  -->  Benched safely until cool!",
        "superpower": "Protects the rest of the team from one buggy robot causing a disaster!",
        "kid_rule": "Bench the dizzy player so the rest of the team stays safe!"
    }
]

def draw_header_bar(c, width, height, s):
    # Top colorful header band
    c.setFillColor(s["tier_color"])
    c.rect(0, height - 58, width, 58, stroke=0, fill=1)

    # Clean text symbol badge on left
    c.setFillColor(colors.white)
    c.roundRect(24, height - 46, 68, 30, 6, stroke=0, fill=1)
    c.setFillColor(s["tier_color"])
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(58, height - 36, s["symbol"])

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(104, height - 37, s["title"])

    # Tier tag on top right
    c.setFont("Helvetica-Bold", 9.5)
    c.drawRightString(width - 24, height - 30, s["tier"].upper())
    c.setFont("Helvetica", 8.5)
    c.drawRightString(width - 24, height - 44, f"Skill #{s['page']} of 20")

def draw_diagram_illustration(c, x, y, w, h, s):
    # Container box for graphic illustration
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 8, stroke=1, fill=1)

    dtype = s["diagram_type"]
    cx = x + w / 2
    cy = y + h / 2

    if dtype == "idea_box":
        # Left: Buzzy Bot Box
        c.setFillColor(colors.HexColor("#fef3c7"))
        c.setStrokeColor(colors.HexColor("#f59e0b"))
        c.roundRect(x + 25, cy - 28, 110, 56, 6, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#b45309"))
        c.setFont("Helvetica-Bold", 9.5)
        c.drawCentredString(x + 80, cy + 8, "Buzzy Bot [Idea]")
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + 80, cy - 8, "(Dreams 100 Ideas)")

        # Arrow
        c.setStrokeColor(colors.HexColor("#64748b"))
        c.setLineWidth(2)
        c.line(x + 145, cy, x + 195, cy)

        # Paper Note
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#94a3b8"))
        c.roundRect(x + 205, cy - 30, 115, 60, 4, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#334155"))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(x + 262, cy + 12, "Idea Blueprint")
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x + 262, cy - 2, "\"Build LEGO Castle\"")
        c.setFillColor(colors.HexColor("#dc2626"))
        c.drawCentredString(x + 262, cy - 16, "[Hands Locked Away]")

        # Arrow
        c.setStrokeColor(colors.HexColor("#64748b"))
        c.line(x + 330, cy, x + 360, cy)

        # Right: Safe Cloud
        c.setFillColor(colors.HexColor("#ecfdf5"))
        c.setStrokeColor(colors.HexColor("#10b981"))
        c.roundRect(x + 370, cy - 28, 140, 56, 6, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#065f46"))
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 440, cy + 6, "Real Cloud World")
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + 440, cy - 10, "Protected & Safe [OK]")

    elif dtype == "guard_gate":
        # Asking Robot
        c.setFillColor(colors.HexColor("#eff6ff"))
        c.setStrokeColor(colors.HexColor("#3b82f6"))
        c.roundRect(x + 25, cy - 28, 110, 56, 6, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#1d4ed8"))
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 80, cy + 6, "Smart Robot")
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x + 80, cy - 10, "\"Can I delete file?\"")

        # Officer Cedar
        c.setFillColor(colors.HexColor("#fee2e2"))
        c.setStrokeColor(colors.HexColor("#dc2626"))
        c.roundRect(x + 165, cy - 32, 160, 64, 8, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#991b1b"))
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + 245, cy + 10, "Officer Cedar [Guard]")
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + 245, cy - 6, "Checks Cedar Rulebook:")
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + 245, cy - 20, "NO PASS = ACCESS DENIED!")

        # Green Door
        c.setFillColor(colors.HexColor("#dcfce7"))
        c.setStrokeColor(colors.HexColor("#16a34a"))
        c.roundRect(x + 355, cy - 28, 155, 56, 6, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#166534"))
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 432, cy + 6, "Principal's Office")
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x + 432, cy - 10, "Hardware Protected")

    elif dtype == "time_capsule":
        c.setFillColor(colors.HexColor("#fef3c7"))
        c.setStrokeColor(colors.HexColor("#d97706"))
        c.roundRect(cx - 150, cy - 30, 300, 60, 10, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#92400e"))
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(cx, cy + 10, "[ S3 WORM TIME CAPSULE SAFE ]")
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(cx, cy - 6, "LOCKED FOR 7 YEARS WITH PADLOCK")
        c.setFont("Helvetica", 8)
        c.drawCentredString(cx, cy - 20, "Zero eraser marks  |  100% Unchangeable Truth")

    elif dtype == "three_columns":
        col_w = (w - 50) / 3
        cols_info = [
            ("LANE 1: FINANCE", "#ede9fe", "#6d28d9", "Money & Liquidity"),
            ("LANE 2: COMPLIANCE", "#dbeafe", "#1e40af", "Hallway Cedar Passes"),
            ("LANE 3: OPERATIONS", "#dcfce7", "#15803d", "LEGO Builder Tasks")
        ]
        for idx, (title, bg, fg, sub) in enumerate(cols_info):
            bx = x + 15 + idx * (col_w + 10)
            c.setFillColor(colors.HexColor(bg))
            c.setStrokeColor(colors.HexColor(fg))
            c.roundRect(bx, cy - 30, col_w, 60, 6, stroke=1, fill=1)
            c.setFillColor(colors.HexColor(fg))
            c.setFont("Helvetica-Bold", 8.5)
            c.drawCentredString(bx + col_w/2, cy + 10, title)
            c.setFont("Helvetica", 7.5)
            c.drawCentredString(bx + col_w/2, cy - 8, sub)

    elif dtype == "quorum_hands":
        c.setFillColor(colors.HexColor("#f5f3ff"))
        c.setStrokeColor(colors.HexColor("#7c3aed"))
        c.roundRect(cx - 170, cy - 30, 340, 60, 8, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#5b21b6"))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString(cx, cy + 10, "SUPERMAJORITY VOTE: 10 OUT OF 12 YES!")
        c.setFont("Helvetica", 8.5)
        c.drawCentredString(cx, cy - 6, "10 Robots Vote YES [Hands Up]  |  2 Glitching Robots Ignored")
        c.setFillColor(colors.HexColor("#16a34a"))
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(cx, cy - 20, "DECISION CERTIFIED & COMMITTED TO WORM VAULT!")

    elif dtype == "clubhouse_shortcuts":
        c.setFillColor(colors.HexColor("#faf5ff"))
        c.setStrokeColor(colors.HexColor("#c084fc"))
        c.roundRect(x + 20, cy - 26, 120, 52, 6, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#6b21a8"))
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 80, cy + 4, "Clubhouse 1")
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x + 80, cy - 10, "(Finance Pod)")

        c.setStrokeColor(colors.HexColor("#a855f7"))
        c.setLineWidth(2)
        c.line(x + 145, cy, x + 205, cy)
        c.drawString(x + 155, cy + 6, "ZIP-LINE")

        c.setFillColor(colors.HexColor("#eff6ff"))
        c.setStrokeColor(colors.HexColor("#93c5fd"))
        c.roundRect(x + 215, cy - 26, 120, 52, 6, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#1e40af"))
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 275, cy + 4, "Clubhouse 2")
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x + 275, cy - 10, "(Compliance Pod)")

        c.setStrokeColor(colors.HexColor("#3b82f6"))
        c.line(x + 340, cy, x + 400, cy)
        c.drawString(x + 350, cy + 6, "ZIP-LINE")

        c.setFillColor(colors.HexColor("#ecfdf5"))
        c.setStrokeColor(colors.HexColor("#86efac"))
        c.roundRect(x + 410, cy - 26, 120, 52, 6, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#065f46"))
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 470, cy + 4, "Clubhouse 3")
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x + 470, cy - 10, "(Operations Pod)")

    else:
        # Default smart diagram box
        c.setFillColor(colors.HexColor("#eff6ff"))
        c.setStrokeColor(colors.HexColor("#3b82f6"))
        c.roundRect(cx - 160, cy - 28, 320, 56, 8, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#1e40af"))
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(cx, cy + 6, f"{s['hero_name']} in Action")
        c.setFont("Helvetica", 8)
        c.drawCentredString(cx, cy - 10, s["diagram_caption"])

    # Bottom caption
    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(cx, y + 8, s["diagram_caption"])

def build_pdf():
    c = canvas.Canvas(PDF_FILENAME, pagesize=letter)
    width, height = letter # 612 x 792

    for s in SKILLS_DATA:
        # 1. Background clean white
        c.setFillColor(colors.HexColor("#ffffff"))
        c.rect(0, 0, width, height, stroke=0, fill=1)

        # 2. Header Bar
        draw_header_bar(c, width, height, s)

        # 3. Sub-header Superhero / Character Name
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setFont("Helvetica-Bold", 15)
        c.drawString(32, height - 85, f"Meet {s['hero_name']}!")

        # 4. One-Liner Box
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.setStrokeColor(s["accent"])
        c.setLineWidth(1.5)
        c.roundRect(32, height - 160, width - 64, 62, 8, stroke=1, fill=1)

        c.setFillColor(colors.HexColor("#64748b"))
        c.setFont("Helvetica-Bold", 8)
        c.drawString(46, height - 116, "WHAT IS THIS SKILL IN ONE SENTENCE?")
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setFont("Helvetica", 10)
        
        # Word wrap one liner
        words = s["one_liner"].split(" ")
        l1, l2 = [], []
        for w in words:
            if c.stringWidth(" ".join(l1 + [w]), "Helvetica", 10) < (width - 100):
                l1.append(w)
            else:
                l2.append(w)
        c.drawString(46, height - 134, " ".join(l1))
        if l2:
            c.drawString(46, height - 149, " ".join(l2))

        # 5. The Storybook Playground Analogy Section
        c.setFillColor(s["accent"])
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(32, height - 188, "The Playground Story (How It Works):")

        c.setFillColor(colors.HexColor("#334155"))
        c.setFont("Helvetica", 9.5)
        
        # Word wrap the story
        words = s["story"].split(" ")
        lines = []
        cur_line = []
        for w in words:
            test = " ".join(cur_line + [w])
            if c.stringWidth(test, "Helvetica", 9.5) < (width - 68):
                cur_line.append(w)
            else:
                lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))

        curr_y = height - 208
        for line in lines:
            c.drawString(32, curr_y, line)
            curr_y -= 15.5

        # 6. Graphical Fun Illustration Diagram
        diag_y = curr_y - 120
        draw_diagram_illustration(c, 32, diag_y, width - 64, 110, s)

        # 7. Superpower Banner
        pow_y = diag_y - 74
        c.setFillColor(s["badge_bg"])
        c.setStrokeColor(s["accent"])
        c.setLineWidth(1)
        c.roundRect(32, pow_y, width - 64, 62, 8, stroke=1, fill=1)

        c.setFillColor(s["badge_fg"])
        c.setFont("Helvetica-Bold", 10)
        c.drawString(46, pow_y + 39, f"Superpower: {s['superpower']}")

        c.setFillColor(colors.HexColor("#0f172a"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(46, pow_y + 17, f"The 4th Grader Golden Rule: \"{s['kid_rule']}\"")

        # 8. Footer Page Info
        c.setStrokeColor(colors.HexColor("#e2e8f0"))
        c.setLineWidth(1)
        c.line(32, 40, width - 32, 40)

        c.setFillColor(colors.HexColor("#94a3b8"))
        c.setFont("Helvetica-Bold", 8)
        c.drawString(32, 26, "THE 3-TIER ENTERPRISE AGENT STACK -- EXPLAINED FOR 4TH GRADERS")
        c.drawRightString(width - 32, 26, f"Page {s['page']} of 20")

        c.showPage()

    c.save()
    print(f"Successfully generated clean 20-page PDF: {PDF_FILENAME}")

if __name__ == "__main__":
    build_pdf()
