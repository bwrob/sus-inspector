
import pytest
from sus_inspector.tui.app import ObjectExplorerApp
from textual.widgets import Tree, OptionList
from sus_inspector.tui.widgets import HistoryModal

@pytest.mark.asyncio
async def test_history_modal_navigation():
    obj = {"a": 1, "b": 2}
    app = ObjectExplorerApp(obj)
    
    async with app.run_test() as pilot:
        tree = app.query_one(Tree)
        
        await pilot.pause()
        
        # root is in history
        # Select "a"
        node_a = None
        for child in tree.root.children:
            if "a" in str(child.label):
                node_a = child
                break
        
        tree.select_node(node_a)
        await pilot.pause()
        
        # Show history
        await pilot.press("ctrl+h")
        await pilot.pause()
        
        assert isinstance(app.screen, HistoryModal)
        
        # History modal should have "root.a" and "root"
        option_list = app.screen.query_one(OptionList)
        assert option_list.option_count == 2
        
        # Select the root option via keyboard.
        await pilot.press("down", "enter")
        
        # Give it plenty of time to dismiss and update
        for _ in range(10):
            await pilot.pause()
        
        # Modal should be dismissed (check query results)
        assert len(app.query(HistoryModal)) == 0
        assert tree.cursor_node == tree.root
        assert app.history_index == 0
