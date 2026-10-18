// Offline resource-model checks for the authored public example.
// This mock is not Minecraft, Mineflayer, a GPT-4 critic, or an upstream API test.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const program = fs.readFileSync(path.join(__dirname, '../examples/voyager.program.js'), 'utf8');
async function run(planks, logs, initialOnly = false) {
  const inventory = {oak_planks: planks, oak_log: logs, chest: 0};
  const calls = [];
  const mcData = {itemsByName: {oak_planks: {id: 'oak_planks'}}};
  const bot = {inventory: {count: id => inventory[id] || 0}};
  const craftItem = async (targetBot, name, batches) => {
    assert.equal(targetBot, bot);
    assert.ok(Number.isInteger(batches) && batches > 0);
    calls.push({name, batches});
    if (name === 'oak_planks') {
      if (inventory.oak_log < batches) return; // Feedback-only material failure.
      inventory.oak_log -= batches;
      inventory.oak_planks += 4 * batches;
    } else if (name === 'chest') {
      if (inventory.oak_planks < 8 * batches) return;
      inventory.oak_planks -= 8 * batches;
      inventory.chest += batches;
    } else {
      throw new Error('Unknown mock recipe');
    }
  };
  await vm.runInNewContext(initialOnly ? 'craftItem(bot, "chest", 1)' : program+'\ncraftChest(bot)', {bot, mcData, craftItem}, {timeout: 1000});
  return {inventory, calls};
}
(async () => {
  const first = await run(6, 1, true);
  assert.equal(first.inventory.chest, 0);
  assert.equal(first.inventory.oak_planks, 6);
  for (const [planks, logs, batches, remaining] of [[6,1,1,2],[0,2,2,0],[8,0,0,0],[10,0,0,2]]) {
    const {inventory, calls} = await run(planks, logs);
    assert.equal(inventory.chest, 1);
    assert.equal(inventory.oak_planks, remaining);
    assert.equal(inventory.oak_log, logs-batches);
    assert.equal(calls.filter(x => x.name==='oak_planks').length, batches ? 1 : 0);
    if (batches) assert.equal(calls[0].batches, batches);
  }
  console.log('Four resource cases and the initial feedback-only failure passed (offline mock).');
})().catch(error => { console.error(error); process.exitCode=1; });
