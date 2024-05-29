# cython: language_level=3

cimport cython

from mc.net.minecraft.client.render.Frustum cimport Frustum
from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.RenderBlocks cimport RenderBlocks
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.World cimport World
from pyglet import gl

cdef int WorldRenderer_chunksUpdates = 0

@cython.final
cdef class WorldRenderer:

    @property
    def chunksUpdates(self):
        return WorldRenderer_chunksUpdates

    @chunksUpdates.setter
    def chunksUpdates(self, x):
        global WorldRenderer_chunksUpdates
        WorldRenderer_chunksUpdates = x

    def __cinit__(self):
        self.__t = tessellator
        self.__glRenderList = -1
        self.isInFrustum = False
        self.needsUpdate = False

    def __init__(self, World world, int posX, int posY, int posZ,
                 int size, int lists, bint fake=False):
        if fake:
            return

        self.__renderBlocks = RenderBlocks(tessellator, world)
        self.__worldObj = world
        self.__posX = posX
        self.__posY = posY
        self.__posZ = posZ
        self.__sizeWidth = 16
        self.__sizeHeight = 16
        self.__sizeDepth = 16
        self.__glRenderList = lists
        self.__setDontDraw()

    cdef updateRenderer(self):
        cdef int layer, x0, y0, z0, xx, yy, zz, x, y, z, blockId
        cdef bint nextLayer, renderPass
        cdef Block block

        self.chunksUpdates += 1

        x0 = self.__posX
        y0 = self.__posY
        z0 = self.__posZ
        xx = self.__posX + self.__sizeWidth
        yy = self.__posY + self.__sizeHeight
        zz = self.__posZ + self.__sizeDepth

        for layer in range(2):
            self.__skipRenderPass[layer] = True

        for layer in range(2):
            nextLayer = False
            renderPass = False

            self.__t.startDrawingQuads()
            gl.glNewList(self.__glRenderList + layer, gl.GL_COMPILE)

            for x in range(x0, xx):
                for y in range(y0, yy):
                    for z in range(z0, zz):
                        blockId = self.__worldObj.getBlockId(x, y, z)
                        if blockId > 0:
                            block = blocks.blocksList[blockId]
                            if block.getRenderBlockPass() != layer:
                                nextLayer = True
                            else:
                                renderPass |= self.__renderBlocks.renderBlockByRenderType(block, x, y, z)

            self.__t.draw()
            gl.glEndList()
            if renderPass:
                self.__skipRenderPass[layer] = False

            if not nextLayer:
                break

    cpdef float distanceToEntitySquared(self, player):
        cdef float xd = player.posX - self.__posX
        cdef float yd = player.posY - self.__posY
        cdef float zd = player.posZ - self.__posZ
        return xd * xd + yd * yd + zd * zd

    cdef __setDontDraw(self):
        cdef int layer
        for layer in range(2):
            self.__skipRenderPass[layer] = True

    def stopRendering(self):
        self.__setDontDraw()
        self.__worldObj = None

    cdef getGLCallListForPass(self, int* chunkBuffer, int startingIndex, int renderPass):
        if not self.isInFrustum:
            return startingIndex

        if not self.__skipRenderPass[renderPass]:
            chunkBuffer[startingIndex] = self.__glRenderList + renderPass
            startingIndex += 1

        return startingIndex

    cdef updateInFrustum(self, Frustum frustum):
        self.isInFrustum = frustum.isBoundingBoxInFrustum(
            self.__posX, self.__posY, self.__posZ, self.__posX + self.__sizeWidth,
            self.__posY + self.__sizeHeight, self.__posZ + self.__sizeDepth
        )
