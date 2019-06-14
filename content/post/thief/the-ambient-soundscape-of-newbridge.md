---
title: "The Ambient Soundscape of Newbridge"
date: 2019-06-14T19:19:51+01:00
draft: false
toc: false
---

## The Goal

In _Making a Profit_, I wanted a rich and dynamic ambient soundscape with two dimensions. Firstly, it would respond to the player’s exploration of the level with regionally-appropriate themes: unsettling whispers in the cemetery, or religious chanting near the Hammerites, for instance. And secondly, to align with the story-driven design of the level, the ambient sound would change and develop alongside the developing plot and enhancing the tension and drama experienced by the player.

As the contest rules allowed only the use of audio files from the game itself, I had a limited palette to work with. Listening to all the available samples and experimenting with different samples playing together, I soon settled on expressing these dimensions with three layers of audio:

The _Tone_ layer is the foundation, with quiet, distant and usually low-frequency sounds. For instance, a low chanting inside the Hammerite’s Sanctuary; or a gentle breeze for the streets. The tone layer primarily reflects the region, and only slightly responds to the plot.

The _Mood_ layer also reflects the region more often than the plot. It complements the Tone, building upon it and enhancing it with detail; on the city streets at the start and end of the mission, it is the sound of crickets chirping on a calm night.

The _Tension_ layer is more distinctly musical, and is the voice of the plot speaking to the player. It varies from neutral, to questioning, to purposeful, to a driving rhythm.

## The Plan

The geography of the level and the plot development are intertwined; my intention was for the Tone, Mood, and Tension all to change separately and smoothly as the player explores and takes action within the level. The city streets is the backbone of the map, and each different region an enclave within it; small and simple in the case of Argaux’s place and the Fishmonger’s shop, or large and multi-layered for the Hammerite Sanctuary, for the cemetery with its mausoleum and hidden catacombs, and for Lady di Rupo’s Manor and the tower leading to the caves and ritual chamber where the mission climax takes place.

<a href="citymap-washed-regions.jpg" title="Click to embiggen" target="_blank"><img src="citymap-washed-regions.jpg" alt="A map of the city, with soundscape regions outlined in different colours. In the west is the Sanctuary exterior, enclosing the sanctuary interior (and by extension its basement and crypt); to the north and south are the small enclaves of Argaux’s place and the Fishmonger’s shop; tn the center is the cemetery, with the mausoleum a small circle in its center; and to the east is the Manor grounds, containing the Manor itself, and on its southernmost edge the Tower, which leads to the Caves, which leads to the Ritual chamber."></a>

The player can only enter each region from the streets, and returns to the streets afterwards. This structure is similar to the hub-and-spoke pattern, only inside-out: the streets are a web-like hub surrounding and enclosing each other region, and each region a spoke which the player enters, explores, acts within, and then leaves again.

The soundscape throughout the mission is supposed to be continuous and yet unobtrusive. And so when it changes, the changes should also be unobtrusive. To this end, usually only one of the three layers changes between adjacent regions as the player moves: for example at the mission start (refer to the diagram below) the tone/mood/tension layers are 🅰ⓐ❶; moving to the sanctuary exterior they become 🅰ⓐ❻ (only the tension changes); returning to the streets and then entering the cemetery or the manor grounds only the tone changes and 🅶ⓐ❶ or 🅺ⓐ❶ plays, respectively.

<a href="citymap-regions.png" title="Click to embiggen" target="_blank"><img src="citymap-regions.png" alt="A table showing the matrix of regions and plot stages, and indicating the three layers of audio that will play for each combination."></a>

But when the plot develops, the soundscape can change two or even three layers at once. For example, when the player learns the details of the job they were hired to do, all three of the layers for the city streets change, from 🅰ⓐ❷ to 🅱ⓑ❸, a shift from an open, inquisitive feeling to a driven, action-inspiring feeling. But it would be quite jarring to hear this change happen all at once. But here the structure of the story and the structure of the soundscape regions work together and avoid that. With one exception, the mission’s plot only develops when the player is within one of these region enclaves; and so each enclaved region’s soundscape remains unchanged with regard to the plot developments that can take place within that region; so the new feeling only comes in when the player returns to the streets to pursue their next objective.

Unfortunately this multidimensional, layered structure is not easy to communicate through text or even diagrams; but with the map and the diagram above, which show the tone/mood/tension layers for each combination of region and plot, you can hopefully get an idea of the flow and change of the soundscape throughout the mission. In total, there are sixteen different tones, thirteen different moods, and twelve different tension layers used in various combinations. The written annotations describe the various feelings that the soundscape expresses.


## The Problem

Typically in Thief, ambient sound and music are put into a level by adding the _AmbientHacked_ property to an object. This either plays as a localised sound with its volume decreasing by the player’s distance from the object, or as a so-called _Environmental_ sound, in which case it is audible at a constant volume everywhere; so ambient music is usually set to be Environmental.

When multiple Environmental AmbientHackeds exist in a level, only one can play at any given time. When the player has line of sight to an Environmental AmbientHacked and approaches within its given radius, then it will begin playing, and any Environmental sounds that were playing before will be stopped. Unfortunately using this radius approach requires placing many AmbientHackeds around the level, often—because Thief levels tend to have complex connectivity—with duplicates around entrances and exits. This is unwieldy, and if you want a rich and varied ambience throughout your level, quickly becomes unmanageable.

As an alternative, you can add the _AmbientHacked_ script to an object with the AmbientHacked property, which will start and stop the sound playing when the object receives _TurnOn_ and _TurnOff_ messages; if it's an Environmental sound, then you can set the radius to zero, and then the sound will play solely based on these messages, regardless of line-of-sight or distance to the player. This allows the Environmental AmbientHacked objects to be placed in a convenient location in the editor (such as an out-of-bounds ‘blue room’), and use roombrush or physics triggers (or even buttons and levers) to control what ambient music is playing as the player moves around your level.

Finally, each AmbientHacked can play not just one, but up to three _schemas_ simultaneously—a schema is either a single sound effect, or a set of sound effects played with some random variation of choice, timing, and panning. It’s no coincidence that I chose to use only three layers in my soundscape, as each layer could be defined by a single schema.

I initially started sketching out the soundscape using radius Environmental AmbientHackeds, but quickly changed to triggered ones once the problems with the former became apparent. To make it easier to develop the soundscapes and schemas, I built a tiny level with a bunch of distinct floor tiles, each corresponding to some combination of region and plot, so that I could simply walk from one tile to another to simulate region or plot changes, and hear the soundscape change accordingly. As the editor allows schema changes to be reloaded without reloading the level, I could switch between the text editor with the schema definitions and the editor running the game for very rapid iteration. This screenshot shows this test level towards the end of the soundscape development, with annotations to remind myself of which floor tile was which:

![A grid of floor tiles: some grass, some cobbled, others with insignia or tombstone inscriptions, that represent the different regions; there are duplicates of each tile for where they change with the plot.](soundscape-test-map.jpg)

Almost immediately an unexpected problem arose: when moving from one area to another, and turning on the new area’s AmbientHacked, the schemas that had been playing all stopped, and the new schemas started from the start—even if they were the same. Which means that moving from one region to another, even with only one different schema in the layers, caused a jarring transition as the ambience stopped and started again. No good at all!

## The Solution

So instead of using AmbientHackeds, I wrote a script that uses the `Sound.PlaySchemaAmbient` and `Sound.HaltSchema` apis to start and stop a set of up to three samples, ensuring that when the set changes, any schemas that are in both the prior set and the new set are left untouched to continue playing. Once again I’m thankful for the addition of Squirrel scripting in NewDark 1.25+, as this problem would’ve been nearly impossible to solve without it.

In addition to solving the transition problem, writing my own script made it possible to enormously simplify the object links in the map. Now, instead of having to link a whole lot of roombrush archetypes to a whole lot of AmbientHacked objects—easy enough to do, but very awkward to maintain or tweak once first done—I could drive the soundscape changes programmatically.

A single object with my _AmbienceController_ script keeps track of the current soundscape region and the plot progression variables, and updates the playing schemas whenever they change. The scripts involved in the plot—that update objectives and so on—send a ‘ProgressChange’ message to the AmbienceController with the new stage of the plot. And a single _PlayerAmbienceWatcher_ script attached to the player sends a ‘RegionChange’ message to the AmbienceController whenever the player enters a new roombrush area. Each roombrush archetype is associated with a particular region by name: “STREETS”, “CATACOMBS” and so on, by means of the ‘Room > Ambient, Schema Name’ property that I added to each of them. (You might wonder what this property is supposed to be used for. The answer is I don’t know; but examining the leaked Thief 2 source code revealed that it’s never actually used; and so I didn’t need to worry about accidentally clashing with any built-in behaviour.)

One last slight hitch remained: in both the catacombs and the ritual chamber, I wanted to change the ambience while the player remained in the same region and while the plot stayed at the same stage. In the catacombs, the change was to encourage the player to run after stealing the Hand (or they’re liable to be killed by an enemy); in the ritual chamber it’s to signal increasing urgency as Lady di Rupo carries out the ritual and gets closer to finishing (which will fail the mission). This was clearly a case of [“special cases aren't special enough to break the rules”](https://www.python.org/dev/peps/pep-0020/), and so for both of these I just defined additional region names—“CATACOMBS2” and so on—and had the relevant scripts modify the room archetype’s ‘Room > Ambient, Schema Name’ property accordingly and send a ‘RegionChange’ message. This is a bit of a hack, but the result is much simpler than trying to fold these changes into the plot progression, let alone adding an independent dimension to represent these changes “properly”. So it’s a good hack.

The final AmbienceController script—which includes the table of each layer’s schemas for each region/plot stage combination—is [on github](https://github.com/adurdin/newbridge/blob/master/sq_scripts/m20_ambience.nut).

**\n**
