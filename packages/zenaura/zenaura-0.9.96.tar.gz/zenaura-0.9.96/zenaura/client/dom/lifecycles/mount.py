from zenaura.client.hydrator import HydratorVirtualDomAdapter

class MountLifeCycles(
    HydratorVirtualDomAdapter
):
    
    async def attached(self, comp) -> None:
        """
        Method called after the component is mounted to the DOM.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        if hasattr(comp, 'attached'):
            await comp.attached()