// Shortened adaptation of MineDojo/Voyager craftChest.js.
// Copyright (c) 2023 MineDojo Team. MIT license;
// see ../references/voyager-code-license.txt.
async function craftChest(bot) {
  const n = bot.inventory.count(
    mcData.itemsByName.oak_planks.id);
  if (n < 8) await craftItem(
    bot, "oak_planks", Math.ceil((8-n)/4));
  await craftItem(bot, "chest", 1);
}
