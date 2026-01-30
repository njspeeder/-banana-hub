-- Banana Hub Platinum Loader
-- Premium Roblox Loader Script v3.0

local HttpService = game:GetService("HttpService")
local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")
local UserInputService = game:GetService("UserInputService")
local Lighting = game:GetService("Lighting")

local player = Players.LocalPlayer
local mouse = player:GetMouse()

-- Configuration (Injected by server or default)
local API_URL = "[[API_URL]]" -- Server will replace this placeholder

-- UI Constants - Enhanced Color Palette
local COLORS = {
    Background = Color3.fromHex("#08080a"),
    BackgroundAlt = Color3.fromHex("#0f0f12"),
    Glass = Color3.fromHex("#141418"),
    GlassLight = Color3.fromHex("#1c1c22"),
    GlassBright = Color3.fromHex("#252530"),
    Accent = Color3.fromHex("#FACC15"),
    AccentDark = Color3.fromHex("#B8960F"),
    AccentGlow = Color3.fromHex("#FDE68A"),
    AccentSoft = Color3.fromHex("#FEF3C7"),
    Secondary = Color3.fromHex("#8B5CF6"),
    SecondaryGlow = Color3.fromHex("#A78BFA"),
    Text = Color3.fromHex("#FAFAFA"),
    TextDim = Color3.fromHex("#A1A1AA"),
    TextMuted = Color3.fromHex("#71717A"),
    TextDark = Color3.fromHex("#52525B"),
    Error = Color3.fromHex("#F87171"),
    ErrorDark = Color3.fromHex("#DC2626"),
    Success = Color3.fromHex("#4ADE80"),
    SuccessGlow = Color3.fromHex("#86EFAC"),
    Border = Color3.fromHex("#27272A"),
    BorderLight = Color3.fromHex("#3f3f46")
}

-- 16:9 Dimensions
local FRAME_WIDTH = 720
local FRAME_HEIGHT = 405

-- Create UI
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "BananaHubLoader"
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
ScreenGui.IgnoreGuiInset = true

-- Try to put in CoreGui if possible, otherwise PlayerGui
local success, err = pcall(function()
    ScreenGui.Parent = CoreGui
end)
if not success then
    ScreenGui.Parent = player:WaitForChild("PlayerGui")
end

-- Add blur effect
local blur = Instance.new("BlurEffect")
blur.Name = "BananaHubBlur"
blur.Size = 0
blur.Parent = Lighting

-- --- UI UTILS ---
local function createCorner(parent, radius)
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, radius or 12)
    corner.Parent = parent
    return corner
end

local function createStroke(parent, color, thickness, transparency)
    local stroke = Instance.new("UIStroke")
    stroke.Color = color or COLORS.Accent
    stroke.Thickness = thickness or 1
    stroke.Transparency = transparency or 0.8
    stroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
    stroke.Parent = parent
    return stroke
end

local function createGradient(parent, colorA, colorB, rotation)
    local gradient = Instance.new("UIGradient")
    gradient.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, colorA),
        ColorSequenceKeypoint.new(1, colorB)
    })
    gradient.Rotation = rotation or 90
    gradient.Parent = parent
    return gradient
end

local function createMultiGradient(parent, keypoints, rotation)
    local gradient = Instance.new("UIGradient")
    gradient.Color = ColorSequence.new(keypoints)
    gradient.Rotation = rotation or 90
    gradient.Parent = parent
    return gradient
end

local function createPadding(parent, top, bottom, left, right)
    local uiPadding = Instance.new("UIPadding")
    uiPadding.PaddingTop = UDim.new(0, top or 0)
    uiPadding.PaddingBottom = UDim.new(0, bottom or top or 0)
    uiPadding.PaddingLeft = UDim.new(0, left or top or 0)
    uiPadding.PaddingRight = UDim.new(0, right or left or top or 0)
    uiPadding.Parent = parent
    return uiPadding
end

local function createShadow(parent, size, transparency)
    local shadow = Instance.new("ImageLabel")
    shadow.Name = "Shadow"
    shadow.AnchorPoint = Vector2.new(0.5, 0.5)
    shadow.BackgroundTransparency = 1
    shadow.Position = UDim2.new(0.5, 0, 0.5, 6)
    shadow.Size = UDim2.new(1, size or 80, 1, size or 80)
    shadow.ZIndex = math.max(1, parent.ZIndex - 1)
    shadow.Image = "rbxassetid://6015667343"
    shadow.ImageColor3 = Color3.new(0, 0, 0)
    shadow.ImageTransparency = transparency or 0.35
    shadow.ScaleType = Enum.ScaleType.Slice
    shadow.SliceCenter = Rect.new(49, 49, 450, 450)
    shadow.Parent = parent
    return shadow
end

local function createGlow(parent, color, size)
    local glow = Instance.new("ImageLabel")
    glow.Name = "Glow"
    glow.AnchorPoint = Vector2.new(0.5, 0.5)
    glow.BackgroundTransparency = 1
    glow.Position = UDim2.new(0.5, 0, 0.5, 0)
    glow.Size = UDim2.new(1, size or 100, 1, size or 100)
    glow.ZIndex = math.max(1, parent.ZIndex - 1)
    glow.Image = "rbxassetid://5028857084"
    glow.ImageColor3 = color or COLORS.Accent
    glow.ImageTransparency = 0.85
    glow.Parent = parent
    return glow
end

local function createList(parent, padding, direction, alignment)
    local list = Instance.new("UIListLayout")
    list.Padding = UDim.new(0, padding or 8)
    list.FillDirection = direction or Enum.FillDirection.Vertical
    list.HorizontalAlignment = alignment or Enum.HorizontalAlignment.Center
    list.SortOrder = Enum.SortOrder.LayoutOrder
    list.Parent = parent
    return list
end

-- Background Overlay with gradient
local BlurOverlay = Instance.new("Frame")
BlurOverlay.Name = "BlurOverlay"
BlurOverlay.BackgroundColor3 = Color3.new(0, 0, 0)
BlurOverlay.BackgroundTransparency = 1
BlurOverlay.Size = UDim2.new(1, 0, 1, 0)
BlurOverlay.ZIndex = 1
BlurOverlay.Parent = ScreenGui

local overlayGradient = Instance.new("UIGradient")
overlayGradient.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0, Color3.fromHex("#0a0a0f")),
    ColorSequenceKeypoint.new(0.5, Color3.fromHex("#000000")),
    ColorSequenceKeypoint.new(1, Color3.fromHex("#0a0512"))
})
overlayGradient.Rotation = 45
overlayGradient.Parent = BlurOverlay

-- Animated background orbs (contained within overlay)
local OrbsContainer = Instance.new("Frame")
OrbsContainer.Name = "Orbs"
OrbsContainer.BackgroundTransparency = 1
OrbsContainer.Size = UDim2.new(1, 0, 1, 0)
OrbsContainer.ClipsDescendants = true
OrbsContainer.ZIndex = 1
OrbsContainer.Parent = BlurOverlay

local function createOrb(position, color, size, duration)
    local orb = Instance.new("Frame")
    orb.Name = "Orb"
    orb.AnchorPoint = Vector2.new(0.5, 0.5)
    orb.BackgroundColor3 = color
    orb.BackgroundTransparency = 0.97
    orb.Position = position
    orb.Size = UDim2.new(0, size, 0, size)
    orb.ZIndex = 1
    orb.Parent = OrbsContainer
    createCorner(orb, size/2)
    
    -- Glow effect
    local orbGlow = Instance.new("ImageLabel")
    orbGlow.BackgroundTransparency = 1
    orbGlow.Size = UDim2.new(1.5, 0, 1.5, 0)
    orbGlow.AnchorPoint = Vector2.new(0.5, 0.5)
    orbGlow.Position = UDim2.new(0.5, 0, 0.5, 0)
    orbGlow.Image = "rbxassetid://5028857084"
    orbGlow.ImageColor3 = color
    orbGlow.ImageTransparency = 0.93
    orbGlow.ZIndex = 1
    orbGlow.Parent = orb
    
    return orb, duration
end

local orbs = {
    createOrb(UDim2.new(0.2, 0, 0.3, 0), COLORS.Accent, 200, 8),
    createOrb(UDim2.new(0.8, 0, 0.7, 0), COLORS.Secondary, 180, 10),
    createOrb(UDim2.new(0.5, 0, 0.25, 0), COLORS.AccentGlow, 150, 12),
}

-- Animate orbs
task.spawn(function()
    while ScreenGui.Parent do
        for i, orbData in ipairs(orbs) do
            local orb, duration = orbData[1], orbData[2]
            if orb and orb.Parent then
                local newPos = UDim2.new(
                    math.random(10, 90) / 100,
                    0,
                    math.random(10, 90) / 100,
                    0
                )
                TweenService:Create(orb, TweenInfo.new(duration, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {
                    Position = newPos,
                    BackgroundTransparency = math.random(95, 98) / 100
                }):Play()
            end
        end
        task.wait(math.random(6, 10))
    end
end)

-- Main Container - 16:9 aspect ratio
local MainFrame = Instance.new("Frame")
MainFrame.Name = "MainFrame"
MainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
MainFrame.BackgroundColor3 = COLORS.Background
MainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
MainFrame.Size = UDim2.new(0, FRAME_WIDTH, 0, FRAME_HEIGHT)
MainFrame.ClipsDescendants = true
MainFrame.ZIndex = 5
MainFrame.Parent = ScreenGui

createCorner(MainFrame, 20)
createShadow(MainFrame, 120, 0.25)

-- Multiple glow layers for depth
local MainGlow1 = createGlow(MainFrame, COLORS.Accent, 300)
MainGlow1.ImageTransparency = 0.94
local MainGlow2 = createGlow(MainFrame, COLORS.Secondary, 200)
MainGlow2.ImageTransparency = 0.96
MainGlow2.Position = UDim2.new(0.7, 0, 0.3, 0)

-- Inner border frame for depth
local InnerBorder = Instance.new("Frame")
InnerBorder.Name = "InnerBorder"
InnerBorder.BackgroundTransparency = 1
InnerBorder.Size = UDim2.new(1, 0, 1, 0)
InnerBorder.ZIndex = 6
InnerBorder.Parent = MainFrame
createCorner(InnerBorder, 20)
local borderStroke = createStroke(InnerBorder, COLORS.Border, 1.5, 0.4)

-- Top accent line with animated gradient
local AccentLine = Instance.new("Frame")
AccentLine.Name = "AccentLine"
AccentLine.BackgroundColor3 = Color3.new(1, 1, 1)
AccentLine.BorderSizePixel = 0
AccentLine.Position = UDim2.new(0, 0, 0, 0)
AccentLine.Size = UDim2.new(1, 0, 0, 3)
AccentLine.ZIndex = 10
AccentLine.Parent = MainFrame

local accentGradient = createMultiGradient(AccentLine, {
    ColorSequenceKeypoint.new(0, COLORS.AccentDark),
    ColorSequenceKeypoint.new(0.3, COLORS.Accent),
    ColorSequenceKeypoint.new(0.5, COLORS.AccentGlow),
    ColorSequenceKeypoint.new(0.7, COLORS.Secondary),
    ColorSequenceKeypoint.new(1, COLORS.SecondaryGlow)
}, 0)

-- Animate the gradient
task.spawn(function()
    local offset = 0
    while ScreenGui.Parent do
        offset = (offset + 0.005) % 1
        accentGradient.Offset = Vector2.new(offset, 0)
        task.wait(0.03)
    end
end)

-- Noise texture overlay
local NoiseOverlay = Instance.new("ImageLabel")
NoiseOverlay.Name = "Noise"
NoiseOverlay.BackgroundTransparency = 1
NoiseOverlay.Size = UDim2.new(1, 0, 1, 0)
NoiseOverlay.Image = "rbxassetid://8137712066"
NoiseOverlay.ImageColor3 = Color3.new(1, 1, 1)
NoiseOverlay.ImageTransparency = 0.97
NoiseOverlay.ScaleType = Enum.ScaleType.Tile
NoiseOverlay.TileSize = UDim2.new(0, 128, 0, 128)
NoiseOverlay.ZIndex = 4
NoiseOverlay.Parent = MainFrame

-- Animated particles container
local ParticlesFrame = Instance.new("Frame")
ParticlesFrame.Name = "Particles"
ParticlesFrame.BackgroundTransparency = 1
ParticlesFrame.Size = UDim2.new(1, 0, 1, 0)
ParticlesFrame.ClipsDescendants = true
ParticlesFrame.ZIndex = 5
ParticlesFrame.Parent = MainFrame

-- Create floating particles with variety
local particles = {}
for i = 1, 20 do
    local particle = Instance.new("Frame")
    particle.Name = "Particle" .. i
    particle.BackgroundColor3 = i % 3 == 0 and COLORS.Secondary or COLORS.Accent
    particle.BackgroundTransparency = math.random(85, 95) / 100
    particle.Position = UDim2.new(math.random() * 0.9 + 0.05, 0, math.random() * 0.9 + 0.05, 0)
    local pSize = math.random(2, 5)
    particle.Size = UDim2.new(0, pSize, 0, pSize)
    particle.ZIndex = 5
    particle.Parent = ParticlesFrame
    createCorner(particle, 10)
    table.insert(particles, particle)
end

-- Animate particles
task.spawn(function()
    while ScreenGui.Parent do
        for _, particle in ipairs(particles) do
            local targetPos = UDim2.new(math.random() * 0.9 + 0.05, 0, math.random() * 0.9 + 0.05, 0)
            TweenService:Create(particle, TweenInfo.new(math.random(5, 12), Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {
                Position = targetPos,
                BackgroundTransparency = math.random(85, 96) / 100
            }):Play()
        end
        task.wait(math.random(4, 7))
    end
end)

-- Dragging Logic
local dragging, dragInput, dragStart, startPos
MainFrame.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
        dragging = true
        dragStart = input.Position
        startPos = MainFrame.Position
        TweenService:Create(MainFrame, TweenInfo.new(0.15, Enum.EasingStyle.Quart), {Size = UDim2.new(0, FRAME_WIDTH + 6, 0, FRAME_HEIGHT + 4)}):Play()
    end
end)

MainFrame.InputChanged:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch then
        dragInput = input
    end
end)

UserInputService.InputChanged:Connect(function(input)
    if input == dragInput and dragging then
        local delta = input.Position - dragStart
        MainFrame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
    end
end)

UserInputService.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
        dragging = false
        TweenService:Create(MainFrame, TweenInfo.new(0.25, Enum.EasingStyle.Back), {Size = UDim2.new(0, FRAME_WIDTH, 0, FRAME_HEIGHT)}):Play()
    end
end)

-- ============================================
-- LOADING SCREEN (Left-aligned for 16:9)
-- ============================================
local LoadingFrame = Instance.new("Frame")
LoadingFrame.Name = "LoadingFrame"
LoadingFrame.BackgroundTransparency = 1
LoadingFrame.Size = UDim2.new(1, 0, 1, 0)
LoadingFrame.ZIndex = 15
LoadingFrame.Parent = MainFrame

-- Animated ring behind logo
local RingContainer = Instance.new("Frame")
RingContainer.Name = "RingContainer"
RingContainer.AnchorPoint = Vector2.new(0.5, 0.5)
RingContainer.BackgroundTransparency = 1
RingContainer.Position = UDim2.new(0.5, 0, 0.42, 0)
RingContainer.Size = UDim2.new(0, 160, 0, 160)
RingContainer.ZIndex = 15
RingContainer.Parent = LoadingFrame

-- Outer spinning ring
local OuterRing = Instance.new("ImageLabel")
OuterRing.Name = "OuterRing"
OuterRing.AnchorPoint = Vector2.new(0.5, 0.5)
OuterRing.BackgroundTransparency = 1
OuterRing.Position = UDim2.new(0.5, 0, 0.5, 0)
OuterRing.Size = UDim2.new(0, 140, 0, 140)
OuterRing.Image = "rbxassetid://7669135072"
OuterRing.ImageColor3 = COLORS.Accent
OuterRing.ImageTransparency = 0.3
OuterRing.ZIndex = 15
OuterRing.Parent = RingContainer

-- Inner spinning ring (opposite direction)
local InnerRing = Instance.new("ImageLabel")
InnerRing.Name = "InnerRing"
InnerRing.AnchorPoint = Vector2.new(0.5, 0.5)
InnerRing.BackgroundTransparency = 1
InnerRing.Position = UDim2.new(0.5, 0, 0.5, 0)
InnerRing.Size = UDim2.new(0, 110, 0, 110)
InnerRing.Image = "rbxassetid://7669135072"
InnerRing.ImageColor3 = COLORS.Secondary
InnerRing.ImageTransparency = 0.5
InnerRing.ZIndex = 15
InnerRing.Parent = RingContainer

-- Logo glow
local LogoGlow = Instance.new("ImageLabel")
LogoGlow.Name = "LogoGlow"
LogoGlow.AnchorPoint = Vector2.new(0.5, 0.5)
LogoGlow.BackgroundTransparency = 1
LogoGlow.Position = UDim2.new(0.5, 0, 0.5, 0)
LogoGlow.Size = UDim2.new(0, 180, 0, 180)
LogoGlow.Image = "rbxassetid://5028857084"
LogoGlow.ImageColor3 = COLORS.Accent
LogoGlow.ImageTransparency = 0.7
LogoGlow.ZIndex = 14
LogoGlow.Parent = RingContainer

-- Logo
local Logo = Instance.new("ImageLabel")
Logo.Name = "Logo"
Logo.AnchorPoint = Vector2.new(0.5, 0.5)
Logo.BackgroundTransparency = 1
Logo.Position = UDim2.new(0.5, 0, 0.5, 0)
Logo.Size = UDim2.new(0, 65, 0, 65)
Logo.Image = "rbxassetid://13192004240"
Logo.ImageColor3 = COLORS.Accent
Logo.ZIndex = 16
Logo.Parent = RingContainer

-- Animate rings spinning
task.spawn(function()
    local rotation = 0
    while LoadingFrame.Visible and ScreenGui.Parent do
        rotation = rotation + 1
        OuterRing.Rotation = rotation
        InnerRing.Rotation = -rotation * 1.5
        task.wait(0.02)
    end
end)

-- Pulsing logo animation
task.spawn(function()
    while LoadingFrame.Visible and ScreenGui.Parent do
        TweenService:Create(Logo, TweenInfo.new(1, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {
            Size = UDim2.new(0, 72, 0, 72)
        }):Play()
        TweenService:Create(LogoGlow, TweenInfo.new(1, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {
            ImageTransparency = 0.5,
            Size = UDim2.new(0, 200, 0, 200)
        }):Play()
        task.wait(1)
        TweenService:Create(Logo, TweenInfo.new(1, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {
            Size = UDim2.new(0, 65, 0, 65)
        }):Play()
        TweenService:Create(LogoGlow, TweenInfo.new(1, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {
            ImageTransparency = 0.7,
            Size = UDim2.new(0, 180, 0, 180)
        }):Play()
        task.wait(1)
    end
end)

-- Title text
local LoadingTitle = Instance.new("TextLabel")
LoadingTitle.Name = "LoadingTitle"
LoadingTitle.AnchorPoint = Vector2.new(0.5, 0.5)
LoadingTitle.BackgroundTransparency = 1
LoadingTitle.Position = UDim2.new(0.5, 0, 0.68, 0)
LoadingTitle.Size = UDim2.new(1, 0, 0, 40)
LoadingTitle.Font = Enum.Font.GothamBlack
LoadingTitle.Text = "BANANA HUB"
LoadingTitle.TextColor3 = COLORS.Text
LoadingTitle.TextSize = 32
LoadingTitle.ZIndex = 15
LoadingTitle.Parent = LoadingFrame

local LoadingSubtitle = Instance.new("TextLabel")
LoadingSubtitle.Name = "LoadingSubtitle"
LoadingSubtitle.AnchorPoint = Vector2.new(0.5, 0.5)
LoadingSubtitle.BackgroundTransparency = 1
LoadingSubtitle.Position = UDim2.new(0.5, 0, 0.75, 0)
LoadingSubtitle.Size = UDim2.new(1, 0, 0, 20)
LoadingSubtitle.Font = Enum.Font.GothamMedium
LoadingSubtitle.Text = "✦ Premium  ✦"
LoadingSubtitle.TextColor3 = COLORS.Accent
LoadingSubtitle.TextSize = 13
LoadingSubtitle.ZIndex = 15
LoadingSubtitle.Parent = LoadingFrame

-- Progress bar container
local ProgressContainer = Instance.new("Frame")
ProgressContainer.Name = "ProgressContainer"
ProgressContainer.AnchorPoint = Vector2.new(0.5, 0.5)
ProgressContainer.BackgroundColor3 = COLORS.Glass
ProgressContainer.Position = UDim2.new(0.5, 0, 0.86, 0)
ProgressContainer.Size = UDim2.new(0, 320, 0, 8)
ProgressContainer.ZIndex = 15
ProgressContainer.Parent = LoadingFrame
createCorner(ProgressContainer, 4)
createStroke(ProgressContainer, COLORS.Border, 1, 0.7)

local Fill = Instance.new("Frame")
Fill.Name = "Fill"
Fill.BackgroundColor3 = COLORS.Accent
Fill.Size = UDim2.new(0, 0, 1, 0)
Fill.ZIndex = 16
Fill.Parent = ProgressContainer
createCorner(Fill, 4)

-- Animated gradient on fill
local fillGradient = createMultiGradient(Fill, {
    ColorSequenceKeypoint.new(0, COLORS.AccentDark),
    ColorSequenceKeypoint.new(0.5, COLORS.Accent),
    ColorSequenceKeypoint.new(1, COLORS.AccentGlow)
}, 0)

-- Shimmer effect on progress bar
local Shimmer = Instance.new("Frame")
Shimmer.Name = "Shimmer"
Shimmer.BackgroundColor3 = Color3.new(1, 1, 1)
Shimmer.BackgroundTransparency = 0.7
Shimmer.Size = UDim2.new(0.3, 0, 1, 0)
Shimmer.Position = UDim2.new(-0.3, 0, 0, 0)
Shimmer.ZIndex = 17
Shimmer.Parent = Fill
createCorner(Shimmer, 4)

task.spawn(function()
    while ScreenGui.Parent do
        Shimmer.Position = UDim2.new(-0.3, 0, 0, 0)
        TweenService:Create(Shimmer, TweenInfo.new(1.5, Enum.EasingStyle.Sine), {Position = UDim2.new(1, 0, 0, 0)}):Play()
        task.wait(2)
    end
end)

-- Progress percentage
local ProgressPercent = Instance.new("TextLabel")
ProgressPercent.Name = "ProgressPercent"
ProgressPercent.AnchorPoint = Vector2.new(1, 0.5)
ProgressPercent.BackgroundTransparency = 1
ProgressPercent.Position = UDim2.new(1, 10, 0.5, 0)
ProgressPercent.Size = UDim2.new(0, 50, 0, 20)
ProgressPercent.Font = Enum.Font.GothamBold
ProgressPercent.Text = "0%"
ProgressPercent.TextColor3 = COLORS.Accent
ProgressPercent.TextSize = 12
ProgressPercent.TextXAlignment = Enum.TextXAlignment.Left
ProgressPercent.ZIndex = 15
ProgressPercent.Parent = ProgressContainer

-- Progress status text
local ProgressText = Instance.new("TextLabel")
ProgressText.Name = "ProgressText"
ProgressText.AnchorPoint = Vector2.new(0.5, 0.5)
ProgressText.BackgroundTransparency = 1
ProgressText.Position = UDim2.new(0.5, 0, 0.93, 0)
ProgressText.Size = UDim2.new(1, 0, 0, 20)
ProgressText.Font = Enum.Font.Gotham
ProgressText.Text = "Initializing..."
ProgressText.TextColor3 = COLORS.TextMuted
ProgressText.TextSize = 11
ProgressText.ZIndex = 15
ProgressText.Parent = LoadingFrame

-- ============================================
-- LOGIN SCREEN (Split layout for 16:9)
-- ============================================
local LoginFrame = Instance.new("Frame")
LoginFrame.Name = "LoginFrame"
LoginFrame.BackgroundTransparency = 1
LoginFrame.Size = UDim2.new(1, 0, 1, 0)
LoginFrame.Visible = false
LoginFrame.ZIndex = 15
LoginFrame.Parent = MainFrame

-- Left Panel (Branding)
local LeftPanel = Instance.new("Frame")
LeftPanel.Name = "LeftPanel"
LeftPanel.BackgroundColor3 = COLORS.BackgroundAlt
LeftPanel.Size = UDim2.new(0.42, 0, 1, 0)
LeftPanel.ZIndex = 15
LeftPanel.Parent = LoginFrame

local leftGradient = createGradient(LeftPanel, COLORS.Background, COLORS.BackgroundAlt, 135)

-- Left panel content container
local LeftContent = Instance.new("Frame")
LeftContent.Name = "LeftContent"
LeftContent.BackgroundTransparency = 1
LeftContent.AnchorPoint = Vector2.new(0.5, 0.5)
LeftContent.Position = UDim2.new(0.5, 0, 0.5, 0)
LeftContent.Size = UDim2.new(0.85, 0, 0.85, 0)
LeftContent.ZIndex = 15
LeftContent.Parent = LeftPanel

-- Brand logo container
local BrandLogo = Instance.new("Frame")
BrandLogo.Name = "BrandLogo"
BrandLogo.BackgroundTransparency = 1
BrandLogo.Size = UDim2.new(1, 0, 0, 90)
BrandLogo.ZIndex = 15
BrandLogo.Parent = LeftContent

local BrandIcon = Instance.new("ImageLabel")
BrandIcon.Name = "BrandIcon"
BrandIcon.BackgroundTransparency = 1
BrandIcon.Size = UDim2.new(0, 55, 0, 55)
BrandIcon.Image = "rbxassetid://13192004240"
BrandIcon.ImageColor3 = COLORS.Accent
BrandIcon.ZIndex = 15
BrandIcon.Parent = BrandLogo

local BrandIconGlow = createGlow(BrandIcon, COLORS.Accent, 50)
BrandIconGlow.ImageTransparency = 0.7

local BrandName = Instance.new("TextLabel")
BrandName.Name = "BrandName"
BrandName.BackgroundTransparency = 1
BrandName.Position = UDim2.new(0, 65, 0, 8)
BrandName.Size = UDim2.new(1, -70, 0, 28)
BrandName.Font = Enum.Font.GothamBlack
BrandName.Text = "BANANA HUB"
BrandName.TextColor3 = COLORS.Text
BrandName.TextSize = 22
BrandName.TextXAlignment = Enum.TextXAlignment.Left
BrandName.ZIndex = 15
BrandName.Parent = BrandLogo

local BrandTag = Instance.new("TextLabel")
BrandTag.Name = "BrandTag"
BrandTag.BackgroundTransparency = 1
BrandTag.Position = UDim2.new(0, 65, 0, 36)
BrandTag.Size = UDim2.new(1, -70, 0, 18)
BrandTag.Font = Enum.Font.GothamMedium
BrandTag.Text = "Premium'/"
BrandTag.TextColor3 = COLORS.Accent
BrandTag.TextSize = 12
BrandTag.TextXAlignment = Enum.TextXAlignment.Left
BrandTag.ZIndex = 15
BrandTag.Parent = BrandLogo

-- Tagline
local Tagline = Instance.new("TextLabel")
Tagline.Name = "Tagline"
Tagline.BackgroundTransparency = 1
Tagline.Position = UDim2.new(0, 0, 0, 100)
Tagline.Size = UDim2.new(1, 0, 0, 60)
Tagline.Font = Enum.Font.GothamBold
Tagline.Text = "Premium Features.\nUnlimited Power."
Tagline.TextColor3 = COLORS.TextDim
Tagline.TextSize = 18
Tagline.TextXAlignment = Enum.TextXAlignment.Left
Tagline.TextYAlignment = Enum.TextYAlignment.Top
Tagline.LineHeight = 1.4
Tagline.ZIndex = 15
Tagline.Parent = LeftContent

-- Feature list
local Features = Instance.new("Frame")
Features.Name = "Features"
Features.BackgroundTransparency = 1
Features.Position = UDim2.new(0, 0, 0, 175)
Features.Size = UDim2.new(1, 0, 0, 160)
Features.ZIndex = 15
Features.Parent = LeftContent

local featureList = {
    {icon = "⚡", text = "Lightning Fast Execution"},
    {icon = "🛡️", text = "Anti-Detection System"},
    {icon = "🎮", text = "Universal Game Support"},
    {icon = "🔄", text = "Auto-Updates Included"}
}

for i, feature in ipairs(featureList) do
    local featureFrame = Instance.new("Frame")
    featureFrame.Name = "Feature" .. i
    featureFrame.BackgroundTransparency = 1
    featureFrame.Position = UDim2.new(0, 0, 0, (i - 1) * 34)
    featureFrame.Size = UDim2.new(1, 0, 0, 30)
    featureFrame.ZIndex = 15
    featureFrame.Parent = Features
    
    local featureIcon = Instance.new("TextLabel")
    featureIcon.BackgroundTransparency = 1
    featureIcon.Size = UDim2.new(0, 24, 1, 0)
    featureIcon.Font = Enum.Font.GothamMedium
    featureIcon.Text = feature.icon
    featureIcon.TextSize = 14
    featureIcon.ZIndex = 15
    featureIcon.Parent = featureFrame
    
    local featureText = Instance.new("TextLabel")
    featureText.BackgroundTransparency = 1
    featureText.Position = UDim2.new(0, 28, 0, 0)
    featureText.Size = UDim2.new(1, -28, 1, 0)
    featureText.Font = Enum.Font.Gotham
    featureText.Text = feature.text
    featureText.TextColor3 = COLORS.TextMuted
    featureText.TextSize = 12
    featureText.TextXAlignment = Enum.TextXAlignment.Left
    featureText.ZIndex = 15
    featureText.Parent = featureFrame
end

-- Right Panel (Login Form)
local RightPanel = Instance.new("Frame")
RightPanel.Name = "RightPanel"
RightPanel.BackgroundTransparency = 1
RightPanel.Position = UDim2.new(0.42, 0, 0, 0)
RightPanel.Size = UDim2.new(0.58, 0, 1, 0)
RightPanel.ZIndex = 15
RightPanel.Parent = LoginFrame

-- Close button
local CloseBtn = Instance.new("TextButton")
CloseBtn.Name = "CloseBtn"
CloseBtn.AnchorPoint = Vector2.new(1, 0)
CloseBtn.BackgroundColor3 = COLORS.Glass
CloseBtn.Position = UDim2.new(1, -20, 0, 20)
CloseBtn.Size = UDim2.new(0, 36, 0, 36)
CloseBtn.Font = Enum.Font.GothamBold
CloseBtn.Text = "✕"
CloseBtn.TextColor3 = COLORS.TextMuted
CloseBtn.TextSize = 16
CloseBtn.AutoButtonColor = false
CloseBtn.ZIndex = 20
CloseBtn.Parent = RightPanel
createCorner(CloseBtn, 10)
createStroke(CloseBtn, COLORS.Border, 1, 0.7)

CloseBtn.MouseEnter:Connect(function()
    TweenService:Create(CloseBtn, TweenInfo.new(0.2), {BackgroundColor3 = COLORS.ErrorDark, TextColor3 = COLORS.Text}):Play()
end)

CloseBtn.MouseLeave:Connect(function()
    TweenService:Create(CloseBtn, TweenInfo.new(0.2), {BackgroundColor3 = COLORS.Glass, TextColor3 = COLORS.TextMuted}):Play()
end)

CloseBtn.MouseButton1Click:Connect(function()
    TweenService:Create(blur, TweenInfo.new(0.4), {Size = 0}):Play()
    local fade = TweenService:Create(MainFrame, TweenInfo.new(0.4, Enum.EasingStyle.Back, Enum.EasingDirection.In), {
        Size = UDim2.new(0, 0, 0, 0),
        BackgroundTransparency = 1
    })
    TweenService:Create(BlurOverlay, TweenInfo.new(0.4), {BackgroundTransparency = 1}):Play()
    for _, orb in ipairs(orbs) do
        if orb[1] then TweenService:Create(orb[1], TweenInfo.new(0.3), {BackgroundTransparency = 1}):Play() end
    end
    fade:Play()
    fade.Completed:Wait()
    blur:Destroy()
    ScreenGui:Destroy()
end)

-- Form container
local FormContainer = Instance.new("Frame")
FormContainer.Name = "FormContainer"
FormContainer.BackgroundTransparency = 1
FormContainer.AnchorPoint = Vector2.new(0.5, 0.5)
FormContainer.Position = UDim2.new(0.5, 0, 0.5, 0)
FormContainer.Size = UDim2.new(0.82, 0, 0.88, 0)
FormContainer.ZIndex = 15
FormContainer.Parent = RightPanel

-- Header
local FormHeader = Instance.new("Frame")
FormHeader.Name = "FormHeader"
FormHeader.BackgroundTransparency = 1
FormHeader.Size = UDim2.new(1, 0, 0, 65)
FormHeader.ZIndex = 15
FormHeader.Parent = FormContainer

local WelcomeText = Instance.new("TextLabel")
WelcomeText.Name = "WelcomeText"
WelcomeText.BackgroundTransparency = 1
WelcomeText.Size = UDim2.new(1, 0, 0, 30)
WelcomeText.Font = Enum.Font.GothamBlack
WelcomeText.Text = "Welcome Back"
WelcomeText.TextColor3 = COLORS.Text
WelcomeText.TextSize = 24
WelcomeText.TextXAlignment = Enum.TextXAlignment.Left
WelcomeText.ZIndex = 15
WelcomeText.Parent = FormHeader

local SubText = Instance.new("TextLabel")
SubText.Name = "SubText"
SubText.BackgroundTransparency = 1
SubText.Position = UDim2.new(0, 0, 0, 32)
SubText.Size = UDim2.new(1, 0, 0, 18)
SubText.Font = Enum.Font.Gotham
SubText.Text = "Enter your credentials to access premium features"
SubText.TextColor3 = COLORS.TextMuted
SubText.TextSize = 12
SubText.TextXAlignment = Enum.TextXAlignment.Left
SubText.ZIndex = 15
SubText.Parent = FormHeader

-- Input Fields
local function createInput(name, placeholder, position, icon)
    local container = Instance.new("Frame")
    container.Name = name .. "Container"
    container.BackgroundColor3 = COLORS.Glass
    container.Position = position
    container.Size = UDim2.new(1, 0, 0, 50)
    container.ZIndex = 15
    container.Parent = FormContainer
    
    createCorner(container, 12)
    local stroke = createStroke(container, COLORS.Border, 1.5, 0.5)
    
    local label = Instance.new("TextLabel")
    label.Name = "Label"
    label.BackgroundTransparency = 1
    label.Position = UDim2.new(0, 0, 0, -22)
    label.Size = UDim2.new(1, 0, 0, 20)
    label.Font = Enum.Font.GothamBold
    label.Text = name:upper()
    label.TextColor3 = COLORS.TextMuted
    label.TextSize = 10
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.ZIndex = 15
    label.Parent = container

    -- Icon background
    local iconBg = Instance.new("Frame")
    iconBg.Name = "IconBg"
    iconBg.BackgroundColor3 = COLORS.GlassLight
    iconBg.Position = UDim2.new(0, 8, 0.5, -16)
    iconBg.Size = UDim2.new(0, 32, 0, 32)
    iconBg.ZIndex = 15
    iconBg.Parent = container
    createCorner(iconBg, 8)

    local iconLabel = Instance.new("TextLabel")
    iconLabel.Name = "Icon"
    iconLabel.BackgroundTransparency = 1
    iconLabel.Size = UDim2.new(1, 0, 1, 0)
    iconLabel.Font = Enum.Font.GothamBold
    iconLabel.Text = icon or "👤"
    iconLabel.TextColor3 = COLORS.TextDim
    iconLabel.TextSize = 14
    iconLabel.ZIndex = 15
    iconLabel.Parent = iconBg

    local input = Instance.new("TextBox")
    input.Name = "Input"
    input.BackgroundTransparency = 1
    input.Position = UDim2.new(0, 50, 0, 0)
    input.Size = UDim2.new(1, -60, 1, 0)
    input.Font = Enum.Font.GothamMedium
    input.PlaceholderText = placeholder
    input.PlaceholderColor3 = COLORS.TextDark
    input.Text = ""
    input.TextColor3 = COLORS.Text
    input.TextSize = 13
    input.TextXAlignment = Enum.TextXAlignment.Left
    input.ClearTextOnFocus = false
    input.ZIndex = 15
    input.Parent = container
    
    -- Focus animations
    input.Focused:Connect(function()
        TweenService:Create(stroke, TweenInfo.new(0.2, Enum.EasingStyle.Quart), {Color = COLORS.Accent, Transparency = 0.2}):Play()
        TweenService:Create(container, TweenInfo.new(0.2, Enum.EasingStyle.Quart), {BackgroundColor3 = COLORS.GlassLight}):Play()
        TweenService:Create(iconBg, TweenInfo.new(0.2), {BackgroundColor3 = COLORS.Accent}):Play()
        TweenService:Create(iconLabel, TweenInfo.new(0.2), {TextColor3 = Color3.new(0, 0, 0)}):Play()
    end)
    
    input.FocusLost:Connect(function()
        TweenService:Create(stroke, TweenInfo.new(0.2, Enum.EasingStyle.Quart), {Color = COLORS.Border, Transparency = 0.5}):Play()
        TweenService:Create(container, TweenInfo.new(0.2, Enum.EasingStyle.Quart), {BackgroundColor3 = COLORS.Glass}):Play()
        TweenService:Create(iconBg, TweenInfo.new(0.2), {BackgroundColor3 = COLORS.GlassLight}):Play()
        TweenService:Create(iconLabel, TweenInfo.new(0.2), {TextColor3 = COLORS.TextDim}):Play()
    end)
    
    return input
end

local UserIDInput = createInput("Discord ID", "Enter your Discord User ID", UDim2.new(0, 0, 0, 88), "🆔")
local KeyInput = createInput("License Key", "BANANA-XXXX-XXXX-XXXX", UDim2.new(0, 0, 0, 168), "🔑")

-- Login Button
local LoginBtn = Instance.new("TextButton")
LoginBtn.Name = "LoginBtn"
LoginBtn.BackgroundColor3 = COLORS.Accent
LoginBtn.Position = UDim2.new(0, 0, 0, 248)
LoginBtn.Size = UDim2.new(1, 0, 0, 50)
LoginBtn.Font = Enum.Font.GothamBlack
LoginBtn.Text = "AUTHENTICATE"
LoginBtn.TextColor3 = Color3.new(0, 0, 0)
LoginBtn.TextSize = 14
LoginBtn.AutoButtonColor = false
LoginBtn.ZIndex = 15
LoginBtn.Parent = FormContainer

createCorner(LoginBtn, 12)

-- Button gradient and glow
local btnGradient = createGradient(LoginBtn, COLORS.AccentDark, COLORS.AccentGlow, 0)

local btnShadow = Instance.new("Frame")
btnShadow.Name = "BtnShadow"
btnShadow.AnchorPoint = Vector2.new(0.5, 0.5)
btnShadow.BackgroundColor3 = COLORS.Accent
btnShadow.BackgroundTransparency = 0.6
btnShadow.Position = UDim2.new(0.5, 0, 0.5, 5)
btnShadow.Size = UDim2.new(1, 0, 1, 0)
btnShadow.ZIndex = 14
btnShadow.Parent = LoginBtn
createCorner(btnShadow, 12)

-- Button icon
local BtnIcon = Instance.new("TextLabel")
BtnIcon.Name = "BtnIcon"
BtnIcon.BackgroundTransparency = 1
BtnIcon.Position = UDim2.new(0, 18, 0, 0)
BtnIcon.Size = UDim2.new(0, 28, 1, 0)
BtnIcon.Font = Enum.Font.GothamBold
BtnIcon.Text = "→"
BtnIcon.TextColor3 = Color3.new(0, 0, 0)
BtnIcon.TextSize = 16
BtnIcon.ZIndex = 15
BtnIcon.Parent = LoginBtn

-- Status message
local Status = Instance.new("TextLabel")
Status.Name = "Status"
Status.BackgroundTransparency = 1
Status.Position = UDim2.new(0, 0, 0, 305)
Status.Size = UDim2.new(1, 0, 0, 22)
Status.Font = Enum.Font.GothamMedium
Status.Text = ""
Status.TextColor3 = COLORS.Error
Status.TextSize = 11
Status.TextXAlignment = Enum.TextXAlignment.Left
Status.ZIndex = 15
Status.Parent = FormContainer

-- Footer
local Footer = Instance.new("Frame")
Footer.Name = "Footer"
Footer.BackgroundTransparency = 1
Footer.AnchorPoint = Vector2.new(0, 1)
Footer.Position = UDim2.new(0, 0, 1, 0)
Footer.Size = UDim2.new(1, 0, 0, 26)
Footer.ZIndex = 15
Footer.Parent = FormContainer

local FooterText = Instance.new("TextLabel")
FooterText.BackgroundTransparency = 1
FooterText.Size = UDim2.new(1, 0, 1, 0)
FooterText.Font = Enum.Font.Gotham
FooterText.Text = "🔒 Secured  •  v3.0  •  © 2026 Banana Hub"
FooterText.TextColor3 = COLORS.TextDark
FooterText.TextSize = 10
FooterText.TextXAlignment = Enum.TextXAlignment.Left
FooterText.ZIndex = 15
FooterText.Parent = Footer

-- ============================================
-- LOGIC
-- ============================================

local function notify(msg, success)
    Status.Text = msg
    Status.TextColor3 = success and COLORS.Success or COLORS.Error
    
    if not success then
        local originalPos = Status.Position
        for i = 1, 3 do
            TweenService:Create(Status, TweenInfo.new(0.04), {Position = originalPos + UDim2.new(0, 6, 0, 0)}):Play()
            task.wait(0.04)
            TweenService:Create(Status, TweenInfo.new(0.04), {Position = originalPos - UDim2.new(0, 6, 0, 0)}):Play()
            task.wait(0.04)
        end
        TweenService:Create(Status, TweenInfo.new(0.04), {Position = originalPos}):Play()
    end
end

local function resolveApiUrl()
    local url = API_URL
    if url == nil or url == "" or url == "[[API_URL]]" then
        local env = (getgenv and getgenv()) or {}
        url = env.API_URL or env.BH_API_URL or env.BANANAHUB_API_URL
    end
    if not url or url == "" or url == "[[API_URL]]" then
        return nil
    end
    url = tostring(url):gsub("/+$", "")
    return url
end

local function requestJson(method, url, body)
    local req = {
        Url = url,
        Method = method,
        Headers = {}
    }
    if body ~= nil then
        req.Headers["Content-Type"] = "application/json"
        req.Body = body
    end
    local ok, res = pcall(function()
        return HttpService:RequestAsync(req)
    end)
    if not ok then
        return false, "request_failed", res
    end
    if not res.Success then
        return false, "http_" .. tostring(res.StatusCode), res
    end
    local decode_ok, data = pcall(function()
        return HttpService:JSONDecode(res.Body)
    end)
    if not decode_ok then
        return false, "decode_failed", res.Body
    end
    return true, data, res
end

local function setButtonLoading(loading)
    if loading then
        LoginBtn.Text = ""
        BtnIcon.Text = ""
        
        local spinner = Instance.new("Frame")
        spinner.Name = "Spinner"
        spinner.BackgroundTransparency = 1
        spinner.AnchorPoint = Vector2.new(0.5, 0.5)
        spinner.Position = UDim2.new(0.5, 0, 0.5, 0)
        spinner.Size = UDim2.new(0, 80, 0, 24)
        spinner.ZIndex = 16
        spinner.Parent = LoginBtn
        
        for i = 1, 3 do
            local dot = Instance.new("Frame")
            dot.Name = "Dot" .. i
            dot.BackgroundColor3 = Color3.new(0, 0, 0)
            dot.Position = UDim2.new(0, (i - 1) * 28 + 6, 0.5, -5)
            dot.Size = UDim2.new(0, 10, 0, 10)
            dot.ZIndex = 17
            dot.Parent = spinner
            createCorner(dot, 5)
            
            task.spawn(function()
                task.wait(i * 0.12)
                while spinner.Parent do
                    TweenService:Create(dot, TweenInfo.new(0.25, Enum.EasingStyle.Quad), {Position = UDim2.new(0, (i - 1) * 28 + 6, 0.5, -12), BackgroundTransparency = 0}):Play()
                    task.wait(0.25)
                    TweenService:Create(dot, TweenInfo.new(0.25, Enum.EasingStyle.Quad), {Position = UDim2.new(0, (i - 1) * 28 + 6, 0.5, -5), BackgroundTransparency = 0.3}):Play()
                    task.wait(0.25)
                end
            end)
        end
        LoginBtn.Active = false
    else
        local spinner = LoginBtn:FindFirstChild("Spinner")
        if spinner then spinner:Destroy() end
        LoginBtn.Text = "AUTHENTICATE"
        BtnIcon.Text = "→"
        LoginBtn.Active = true
    end
end

local function handleLogin()
    local uid = UserIDInput.Text
    local key = KeyInput.Text
    
    if uid == "" or key == "" then
        notify("??? Please fill in all fields", false)
        return
    end
    
    local apiUrl = resolveApiUrl()
    if not apiUrl then
        notify("??? API URL not configured", false)
        return
    end
    
    notify("??? Authenticating...", true)
    setButtonLoading(true)
    
    local query = "user_id=" .. HttpService:UrlEncode(uid) .. "&key=" .. HttpService:UrlEncode(key)
    local ok, dataOrErr = requestJson("GET", apiUrl .. "/api/verify?" .. query)
    
    if not ok then
        -- Fallback for servers that only support /api/auth (JSON POST)
        local payload = HttpService:JSONEncode({uid = uid, user_id = uid, key = key})
        ok, dataOrErr = requestJson("POST", apiUrl .. "/api/auth", payload)
    end
    
    if ok then
        local data = dataOrErr
        local successFlag = data.success == true or data.authenticated == true or data.valid == true
        if successFlag then
            notify("??? Access Granted!", true)
            
            TweenService:Create(LoginBtn, TweenInfo.new(0.3), {BackgroundColor3 = COLORS.Success}):Play()
            setButtonLoading(false)
            LoginBtn.Text = "??? SUCCESS"
            BtnIcon.Text = "???"
            
            task.wait(1)
            
            -- Epic exit animation
            TweenService:Create(blur, TweenInfo.new(0.6), {Size = 0}):Play()
            TweenService:Create(BlurOverlay, TweenInfo.new(0.6), {BackgroundTransparency = 1}):Play()
            
            for _, orb in ipairs(orbs) do
                if orb[1] then TweenService:Create(orb[1], TweenInfo.new(0.4), {BackgroundTransparency = 1}):Play() end
            end
            
            local fadeOut = TweenService:Create(MainFrame, TweenInfo.new(0.6, Enum.EasingStyle.Back, Enum.EasingDirection.In), {
                Size = UDim2.new(0, 0, 0, 0),
                BackgroundTransparency = 1
            })
            fadeOut:Play()
            fadeOut.Completed:Wait()
            blur:Destroy()
            ScreenGui:Destroy()
            
            print("[Banana Hub] Loader finished successfully.")
        else
            local errMsg = data.error or data.message or data.reason or "Invalid credentials"
            notify("??? " .. tostring(errMsg), false)
            setButtonLoading(false)
            
            local originalPos = LoginBtn.Position
            for i = 1, 2 do
                TweenService:Create(LoginBtn, TweenInfo.new(0.04), {Position = originalPos + UDim2.new(0, 10, 0, 0)}):Play()
                task.wait(0.04)
                TweenService:Create(LoginBtn, TweenInfo.new(0.04), {Position = originalPos - UDim2.new(0, 10, 0, 0)}):Play()
                task.wait(0.04)
            end
            TweenService:Create(LoginBtn, TweenInfo.new(0.04), {Position = originalPos}):Play()
        end
    else
        local errLabel = tostring(dataOrErr or "")
        local msg = "??? Connection failed"
        if errLabel ~= "" then
            msg = msg .. " (" .. errLabel .. ")"
        end
        notify(msg, false)
        setButtonLoading(false)
    end
end

-- Button Hover Effects
LoginBtn.MouseEnter:Connect(function()
    TweenService:Create(LoginBtn, TweenInfo.new(0.2, Enum.EasingStyle.Quart), {
        Size = UDim2.new(1, 4, 0, 52),
        Position = UDim2.new(0, -2, 0, 247)
    }):Play()
    TweenService:Create(btnShadow, TweenInfo.new(0.2), {BackgroundTransparency = 0.4, Position = UDim2.new(0.5, 0, 0.5, 8)}):Play()
    TweenService:Create(BtnIcon, TweenInfo.new(0.2), {Position = UDim2.new(0, 23, 0, 0)}):Play()
end)

LoginBtn.MouseLeave:Connect(function()
    TweenService:Create(LoginBtn, TweenInfo.new(0.2, Enum.EasingStyle.Quart), {
        Size = UDim2.new(1, 0, 0, 50),
        Position = UDim2.new(0, 0, 0, 248)
    }):Play()
    TweenService:Create(btnShadow, TweenInfo.new(0.2), {BackgroundTransparency = 0.6, Position = UDim2.new(0.5, 0, 0.5, 5)}):Play()
    TweenService:Create(BtnIcon, TweenInfo.new(0.2), {Position = UDim2.new(0, 18, 0, 0)}):Play()
end)

LoginBtn.MouseButton1Down:Connect(function()
    TweenService:Create(LoginBtn, TweenInfo.new(0.08), {
        Size = UDim2.new(1, -4, 0, 48),
        Position = UDim2.new(0, 2, 0, 249)
    }):Play()
end)

LoginBtn.MouseButton1Up:Connect(function()
    TweenService:Create(LoginBtn, TweenInfo.new(0.08), {
        Size = UDim2.new(1, 4, 0, 52),
        Position = UDim2.new(0, -2, 0, 247)
    }):Play()
end)

LoginBtn.MouseButton1Click:Connect(handleLogin)

-- ============================================
-- LOADING ANIMATION
-- ============================================
task.spawn(function()
    local loadSteps = {
        {progress = 0.15, text = "Initializing core modules..."},
        {progress = 0.30, text = "Loading security layer..."},
        {progress = 0.50, text = "Connecting to servers..."},
        {progress = 0.70, text = "Verifying integrity..."},
        {progress = 0.85, text = "Preparing interface..."},
        {progress = 1.00, text = "Ready to authenticate!"}
    }
    
    for _, step in ipairs(loadSteps) do
        TweenService:Create(Fill, TweenInfo.new(0.4, Enum.EasingStyle.Quart), {Size = UDim2.new(step.progress, 0, 1, 0)}):Play()
        ProgressPercent.Text = math.floor(step.progress * 100) .. "%"
        ProgressText.Text = step.text
        task.wait(0.45)
    end
    
    task.wait(0.4)
    
    -- Fade out loading elements
    local fadeElements = {LoadingTitle, LoadingSubtitle, ProgressContainer, ProgressText, ProgressPercent}
    for _, element in ipairs(fadeElements) do
        if element:IsA("TextLabel") then
            TweenService:Create(element, TweenInfo.new(0.35), {TextTransparency = 1}):Play()
        elseif element:IsA("Frame") then
            TweenService:Create(element, TweenInfo.new(0.35), {BackgroundTransparency = 1}):Play()
        end
    end
    
    TweenService:Create(RingContainer, TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.In), {
        Size = UDim2.new(0, 0, 0, 0)
    }):Play()
    
    task.wait(0.5)
    
    LoadingFrame.Visible = false
    LoginFrame.Visible = true
    
    -- Animate login panel in
    LeftPanel.Position = UDim2.new(-0.42, 0, 0, 0)
    RightPanel.BackgroundTransparency = 1
    
    TweenService:Create(LeftPanel, TweenInfo.new(0.6, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {
        Position = UDim2.new(0, 0, 0, 0)
    }):Play()
    
    task.wait(0.15)
    
    -- Stagger in form elements
    local formElements = {WelcomeText, SubText}
    for i, element in ipairs(formElements) do
        element.TextTransparency = 1
        task.delay(i * 0.08, function()
            TweenService:Create(element, TweenInfo.new(0.4), {TextTransparency = 0}):Play()
        end)
    end
    
    -- Animate input containers
    for _, child in ipairs(FormContainer:GetChildren()) do
        if child:IsA("Frame") and child.Name:find("Container") then
            child.BackgroundTransparency = 1
            task.delay(0.25, function()
                TweenService:Create(child, TweenInfo.new(0.4, Enum.EasingStyle.Quart), {BackgroundTransparency = 0}):Play()
            end)
        end
    end
    
    -- Animate button
    LoginBtn.BackgroundTransparency = 1
    task.delay(0.4, function()
        TweenService:Create(LoginBtn, TweenInfo.new(0.4, Enum.EasingStyle.Quart), {BackgroundTransparency = 0}):Play()
    end)
    
    -- Animate features list
    for i, child in ipairs(Features:GetChildren()) do
        if child:IsA("Frame") then
            for _, label in ipairs(child:GetChildren()) do
                if label:IsA("TextLabel") then
                    label.TextTransparency = 1
                end
            end
            task.delay(0.3 + (i * 0.1), function()
                for _, label in ipairs(child:GetChildren()) do
                    if label:IsA("TextLabel") then
                        TweenService:Create(label, TweenInfo.new(0.4), {TextTransparency = 0}):Play()
                    end
                end
            end)
        end
    end
end)

-- ============================================
-- INITIAL ENTRANCE ANIMATION
-- ============================================
MainFrame.Size = UDim2.new(0, 0, 0, 0)
MainFrame.BackgroundTransparency = 1
BlurOverlay.BackgroundTransparency = 1

-- Animate blur in
TweenService:Create(blur, TweenInfo.new(0.6), {Size = 12}):Play()
TweenService:Create(BlurOverlay, TweenInfo.new(0.5), {BackgroundTransparency = 0.4}):Play()

-- Animate main frame in with bounce
TweenService:Create(MainFrame, TweenInfo.new(0.7, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {
    Size = UDim2.new(0, FRAME_WIDTH, 0, FRAME_HEIGHT),
    BackgroundTransparency = 0
}):Play()
