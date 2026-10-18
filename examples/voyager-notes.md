# Voyager: public example and design evidence

[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291), Wang et al., 2023; [official project](https://voyager.minedojo.org/). Read Sections 2.1–2.3 and Figures 2–6. The diagram explains an automatic curriculum, an executable skill library, and iterative code learning through environment feedback, interpreter errors and self-verification.

Implementation references are pinned to [MineDojo/Voyager revision 55e45a880755d0c8c66ca7fb5fe7962ac8974f89](https://github.com/MineDojo/Voyager/tree/55e45a880755d0c8c66ca7fb5fe7962ac8974f89): `voyager/agents/skill.py`, `critic.py`, `voyager/voyager.py`, `voyager/control_primitives/craftItem.js`, and `skill_library/trial1/skill/code/craftChest.js`. The functional chest-code excerpt shortens the released MIT-licensed program; the upstream copyright/license notice is retained. The composition, schematic world, recipe shapes and illustrative state sequence are independently authored.

## Concrete explanatory choices

| Reader question | Visible mechanism |
|---|---|
| Where does a new objective come from? | World state, exploration history and GPT-3.5 context support a novel, feasible GPT-4 task |
| What do stored skills contribute? | A query vector retrieves up to five relevant programs, supplied as action-agent context |
| What changes after a failure? | The initial chest call lacks materials; a resource-aware code excerpt converts wood before retrying |
| Does finishing code prove the task succeeded? | The first interpreter channel is empty while inventory and critic still indicate failure |
| What is learned? | A verified program is described, indexed by description embedding, and stored as executable code |

The synthetic task starts with one oak log, six oak planks, no chest, and a nearby crafting table. The eight-plank recipe is illustrated with native data shapes. One plank-recipe batch consumes one log and makes four planks: six becomes ten; crafting one chest consumes eight and leaves two. The source `craftItem` argument is recipe batches, not output item units. The displayed correction reads the current plank count instead of hard-coding the six-plank instance. Its full wrapper is in `voyager.program.js`.

The numerical trace is offline accounting. The optional Node test executes the authored JavaScript against a small resource mock across four inventories and an initial feedback-only failure. It does not run Minecraft, Mineflayer, Voyager, an embedding service or any LLM. The depicted curriculum choice, retrieved entries, critic language, description and vectors are illustrative. The five entries are plausible descriptions of released skill types, not a captured retrieval ranking. The frontier is an example learning trajectory, not a fixed curriculum. The four-attempt budget is the paper/default setting and is configurable in code.

## Visual transfer

This second example deliberately changes composition: an apricot curriculum spans the top, a large lavender code/environment scene anchors the lower left, and teal retrieval/storage occupies the right. The primary explanation uses a native voxel inset, recipe grid, resource transitions and program edit, rather than geometric proof nodes. Professional operation icons have useful visible size in headers and payloads. Auxiliary blue, amber, rose and mint distinguish states while large surfaces remain pale. Comic Sans MS and the same rounded dashed hierarchy connect the examples stylistically.

Texts, code, state cards, recipe cells, vector marks and world faces are editable native draw.io objects. World faces use original compressed native stencil definitions. No Minecraft textures, game screenshots, PDF paths or paper images are shipped. The drawn world is a schematic and the chest is a stock illustration. Icons: [Free icons from Streamline](https://www.streamlinehq.com/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); exact original bytes and sources are in the shared ledger. Code adaptation: [upstream MIT notice](../references/voyager-code-license.txt).

Both public examples are author-designed and author-reviewed. Their existence does not establish independent-agent transfer performance or guarantee future aesthetic quality. Apply the scientific reading and actual-render review workflow again for new papers.
