from mc.net.minecraft.client.controller.PlayerControllerSP import PlayerControllerSP
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.gui.ScaledResolution import ScaledResolution
from mc.net.minecraft.client.gui.Gui import Gui
from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.client.ChatLine import ChatLine
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.JavaUtils import Random
from pyglet import window, gl
import math

class GuiIngame(Gui):
    __rand = Random()

    def __init__(self, minecraft):
        self.__mc = minecraft
        self.__blockRenderer = RenderBlocks(tessellator)
        self.__chatMessageList = []
        self.__updateCounter = 0

    def renderGameOverlay(self, a):
        scaledRes = ScaledResolution(self.__mc.width, self.__mc.height)
        scaledWidth = scaledRes.getScaledWidth()
        scaledHeight = scaledRes.getScaledHeight()
        self.__mc.entityRenderer.setupOverlayRendering()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('gui/gui.png'))
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_BLEND)
        self._zLevel = -90.0
        self.drawTexturedModalRect(scaledWidth / 2 - 91, scaledHeight - 22, 0, 0, 182, 22)
        self.drawTexturedModalRect(scaledWidth / 2 - 91 - 1 + self.__mc.thePlayer.inventory.currentItem * 20,
                                   scaledHeight - 22 - 1, 0, 22, 24, 22)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__mc.renderEngine.getTexture('gui/icons.png'))
        self.drawTexturedModalRect(scaledWidth / 2 - 7, scaledHeight / 2 - 7, 0, 0, 16, 16)
        invulnerable = 1 if self.__mc.thePlayer.heartsLife // 3 % 2 == 1 else 0
        if self.__mc.thePlayer.heartsLife < 10:
            invulnerable = 0

        health = self.__mc.thePlayer.health
        prevHealth = self.__mc.thePlayer.prevHealth
        self.__rand.setSeed(self.__updateCounter * 312871)
        if self.__mc.playerController.shouldDrawHUD():
            for i in range(10):
                n5 = 0
                if invulnerable != 0:
                    n5 = 1

                n4 = scaledWidth / 2 - 91 + (i << 3)
                n3 = scaledHeight - 32
                if health <= 4:
                    n3 += self.__rand.nextInt(2)

                self.drawTexturedModalRect(n4, n3, 16 + n5 * 9, 0, 9, 9)
                if invulnerable != 0:
                    if (i << 1) + 1 < prevHealth:
                        self.drawTexturedModalRect(n4, n3, 70, 0, 9, 9)
                    elif (i << 1) + 1 == prevHealth:
                        self.drawTexturedModalRect(n4, n3, 79, 0, 9, 9)

                if (i << 1) + 1 < health:
                    self.drawTexturedModalRect(n4, n3, 52, 0, 9, 9)
                elif (i << 1) + 1 == health:
                    self.drawTexturedModalRect(n4, n3, 61, 0, 9, 9)

            if self.__mc.thePlayer.isInsideOfMaterial():
                n6 = math.ceil((self.__mc.thePlayer.air - 2) * 10.0 / 300.0)
                n5 = math.ceil(self.__mc.thePlayer.air * 10.0 / 300.0) - n6
                for n4 in range(n6 + n5):
                    if n4 < n6:
                        self.drawTexturedModalRect(scaledWidth / 2 - 91 + (n4 << 3),
                                                   scaledHeight - 32 - 9, 16, 18, 9, 9)
                    else:
                        self.drawTexturedModalRect(scaledWidth / 2 - 91 + (n4 << 3),
                                                   scaledHeight - 32 - 9, 25, 18, 9, 9)

        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_NORMALIZE)
        gl.glPushMatrix()
        gl.glRotatef(180.0, 1.0, 0.0, 0.0)
        RenderHelper.enableStandardItemLighting()
        gl.glPopMatrix()

        for slot in range(9):
            width = scaledWidth // 2 - 90 + slot * 20 + 2
            height = scaledHeight - 16 - 3
            stack = self.__mc.thePlayer.inventory.mainInventory[slot]
            if not stack:
                if slot > 50:
                    gl.glDisable(gl.GL_LIGHTING)
                    tex = this.mc.renderEngine.getTexture('gui/items.png')
                    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                    self.drawTexturedModalRect(width, height, 240, 63 - slot << 4, 16, 16)
                    gl.glEnable(gl.GL_LIGHTING)

                continue

            anim = stack.animationsToGo - a
            if anim > 0.0:
                gl.glPushMatrix()
                s = 1.0 + anim / 5.0
                gl.glTranslatef(width + 8, height + 12, 0.0)
                gl.glScalef(1.0 / s, (s + 1.0) / 2.0, 1.0)
                gl.glTranslatef(-(width + 8), -(height + 12), 0.0)

            item = stack.itemID
            if item < 256:
                tex = self.__mc.renderEngine.getTexture('terrain.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                block = blocks.blocksList[item]
                gl.glPushMatrix()
                gl.glTranslatef(width - 2, height + 3, 0.0)
                gl.glScalef(10.0, 10.0, 10.0)
                gl.glTranslatef(1.0, 0.5, 8.0)
                gl.glRotatef(210.0, 1.0, 0.0, 0.0)
                gl.glRotatef(45.0, 0.0, 1.0, 0.0)
                gl.glColor4f(1.0, 1.0, 1.0, 1.0)
                self.__blockRenderer.renderBlockOnInventory(block)
                gl.glPopMatrix()
            elif stack.getItem().getIconIndex() >= 0:
                gl.glDisable(gl.GL_LIGHTING)
                tex = self.__mc.renderEngine.getTexture('gui/items.png')
                gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
                self.drawTexturedModalRect(
                    width, height, stack.getItem().getIconIndex() % 16 << 4,
                    stack.getItem().getIconIndex() // 16 << 4, 16, 16
                )
                gl.glEnable(gl.GL_LIGHTING)

            if anim > 0.0:
                gl.glPopMatrix()

            if stack.stackSize > 1:
                size = str(stack.stackSize)
                gl.glDisable(gl.GL_LIGHTING)
                gl.glDisable(gl.GL_DEPTH_TEST)
                self.__mc.fontRenderer.drawStringWithShadow(
                    size, width + 19 - 2 - self.__mc.fontRenderer.getStringWidth(size),
                    height + 6 + 3, 16777215)
                gl.glEnable(gl.GL_LIGHTING)
                gl.glEnable(gl.GL_DEPTH_TEST)

        RenderHelper.disableStandardItemLighting()
        gl.glDisable(gl.GL_NORMALIZE)
        self.__mc.fontRenderer.drawStringWithShadow(self.__mc.VERSION_STRING, 2, 2, 0xFFFFFF)
        if self.__mc.options.showFPS:
            self.__mc.fontRenderer.drawStringWithShadow(self.__mc.debug, 2, 12, 0xFFFFFF)

        if isinstance(self.__mc.playerController, PlayerControllerSP):
            score = 'Score: &e' + str(self.__mc.thePlayer.getScore())
            self.__mc.fontRenderer.drawStringWithShadow(
                score, scaledWidth - self.__mc.fontRenderer.getStringWidth(score) - 2,
                2, 16777215
            )

        for i, message in enumerate(self.__chatMessageList):
            if i >= 10:
                break

            if message.updateCounter < 200:
                self.__mc.fontRenderer.drawStringWithShadow(
                    None, 2, scaledHeight - 8 - i * 9 - 20, 0xFFFFFF
                )

    def addChatMessage(self):
        self.__updateCounter += 1
        for message in self.__chatMessageList.copy():
            message.updateCounter += 1
