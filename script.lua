-- Banana Hub Loader (Modern UI + Landing)
-- v4.2

local HttpService = game:GetService("HttpService")
local TweenService = game:GetService("TweenService")
local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")
local UserInputService = game:GetService("UserInputService")
local Lighting = game:GetService("Lighting")

local player = Players.LocalPlayer

local API_URL = "[[API_URL]]"
local DEFAULT_API_URL = "https://banana-hub.onrender.com"

local COLORS = {
    Bg = Color3.fromHex("#0b0c10"),
    Bg2 = Color3.fromHex("#10141c"),
    Panel = Color3.fromHex("#141822"),
    PanelHi = Color3.fromHex("#1a2030"),
    Accent = Color3.fromHex("#f5c400"),
    Accent2 = Color3.fromHex("#ff8a00"),
    Text = Color3.fromHex("#f8fafc"),
    Muted = Color3.fromHex("#9aa4b2"),
    Border = Color3.fromHex("#2a2f3a"),
    Error = Color3.fromHex("#ef4444"),
    Success = Color3.fromHex("#22c55e")
}

local function createCorner(parent, radius)
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, radius or 10)
    corner.Parent = parent
    return corner
end

local function createStroke(parent, color, thickness, transparency)
    local stroke = Instance.new("UIStroke")
    stroke.Color = color or COLORS.Border
    stroke.Thickness = thickness or 1
    stroke.Transparency = transparency or 0
    stroke.Parent = parent
    return stroke
end

local function createGradient(parent, c1, c2, rotation)
    local grad = Instance.new("UIGradient")
    grad.Color = ColorSequence.new(c1, c2)
    grad.Rotation = rotation or 90
    grad.Parent = parent
    return grad
end

local function resolveApiUrl()
    local url = API_URL
    if url == nil or url == "" or url == "[[API_URL]]" then
        local env = (getgenv and getgenv()) or {}
        url = env.API_URL or env.BH_API_URL or env.BANANAHUB_API_URL
    end
    if not url or url == "" or url == "[[API_URL]]" then
        url = DEFAULT_API_URL
    end
    if not url or url == "" or url == "[[API_URL]]" then
        return nil
    end
    url = tostring(url):gsub("/+$", "")
    return url
end

local function requestJson(method, url, body)
    local req = { Url = url, Method = method, Headers = {} }
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

-- UI setup
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "BananaHubLoader"
ScreenGui.ResetOnSpawn = false
ScreenGui.IgnoreGuiInset = true
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

pcall(function() ScreenGui.Parent = CoreGui end)
if not ScreenGui.Parent then
    ScreenGui.Parent = player:WaitForChild("PlayerGui")
end

local blur = Instance.new("BlurEffect")
blur.Name = "BananaHubBlur"
blur.Size = 0
blur.Parent = Lighting

local Root = Instance.new("Frame")
Root.Name = "Root"
Root.Size = UDim2.new(1, 0, 1, 0)
Root.BackgroundColor3 = COLORS.Bg
Root.BackgroundTransparency = 0.65
Root.BorderSizePixel = 0
Root.Parent = ScreenGui
createGradient(Root, COLORS.Bg, COLORS.Bg2, 45)

-- Subtle noise texture
local Noise = Instance.new("ImageLabel")
Noise.Name = "Noise"
Noise.BackgroundTransparency = 1
Noise.Size = UDim2.new(1, 0, 1, 0)
Noise.Image = "rbxassetid://8137712066"
Noise.ImageTransparency = 0.96
Noise.ScaleType = Enum.ScaleType.Tile
Noise.TileSize = UDim2.new(0, 128, 0, 128)
Noise.ZIndex = 2
Noise.Parent = Root
Noise.Visible = false

-- Floating orbs
local OrbA = Instance.new("Frame")
OrbA.BackgroundColor3 = COLORS.Accent
OrbA.BackgroundTransparency = 1
OrbA.Size = UDim2.new(0, 220, 0, 220)
OrbA.Position = UDim2.new(0.15, 0, 0.3, 0)
OrbA.Parent = Root
createCorner(OrbA, 999)

local OrbB = Instance.new("Frame")
OrbB.BackgroundColor3 = COLORS.Accent2
OrbB.BackgroundTransparency = 1
OrbB.Size = UDim2.new(0, 260, 0, 260)
OrbB.Position = UDim2.new(0.7, 0, 0.6, 0)
OrbB.Parent = Root
createCorner(OrbB, 999)

local function floatOrb(orb, duration)
    task.spawn(function()
        while orb.Parent do
            local nx = math.random(10, 90) / 100
            local ny = math.random(10, 90) / 100
            TweenService:Create(orb, TweenInfo.new(duration, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {
                Position = UDim2.new(nx, 0, ny, 0),
                BackgroundTransparency = math.random(85, 93) / 100
            }):Play()
            task.wait(duration + 0.2)
        end
    end)
end

floatOrb(OrbA, 9)
floatOrb(OrbB, 12)

-- Main container
local Card = Instance.new("Frame")
Card.Name = "Card"
Card.AnchorPoint = Vector2.new(0.5, 0.5)
Card.Position = UDim2.new(0.5, 0, 0.5, 0)
Card.Size = UDim2.new(0, 720, 0, 380)
Card.BackgroundColor3 = COLORS.Panel
Card.Parent = Root
createCorner(Card, 18)
createStroke(Card, COLORS.Border, 1, 0.35)

local CardShadow = Instance.new("ImageLabel")
CardShadow.Name = "Shadow"
CardShadow.AnchorPoint = Vector2.new(0.5, 0.5)
CardShadow.BackgroundTransparency = 1
CardShadow.Position = UDim2.new(0.5, 0, 0.5, 8)
CardShadow.Size = UDim2.new(1, 140, 1, 140)
CardShadow.Image = "rbxassetid://6015667343"
CardShadow.ImageColor3 = Color3.new(0, 0, 0)
CardShadow.ImageTransparency = 0.5
CardShadow.ScaleType = Enum.ScaleType.Slice
CardShadow.SliceCenter = Rect.new(49, 49, 450, 450)
CardShadow.ZIndex = 0
CardShadow.Parent = Card

local AccentBar = Instance.new("Frame")
AccentBar.BackgroundColor3 = COLORS.Accent
AccentBar.Size = UDim2.new(1, 0, 0, 3)
AccentBar.Parent = Card
createCorner(AccentBar, 4)
createGradient(AccentBar, COLORS.Accent, COLORS.Accent2, 0)

-- Left feature strip
local LeftPanel = Instance.new("Frame")
LeftPanel.Name = "LeftPanel"
LeftPanel.BackgroundColor3 = COLORS.PanelHi
LeftPanel.Size = UDim2.new(0, 260, 1, -3)
LeftPanel.Position = UDim2.new(0, 0, 0, 3)
LeftPanel.Parent = Card
createCorner(LeftPanel, 18)
createStroke(LeftPanel, COLORS.Border, 1, 0.4)

local LeftGradient = createGradient(LeftPanel, Color3.fromHex("#161c27"), Color3.fromHex("#10141c"), 130)
LeftGradient.Offset = Vector2.new(0, 0)

-- Animated logo
local Logo = Instance.new("ImageLabel")
Logo.BackgroundTransparency = 1
Logo.Image = "rbxassetid://13192004240"
Logo.ImageColor3 = COLORS.Accent
Logo.Size = UDim2.new(0, 56, 0, 56)
Logo.Position = UDim2.new(0, 24, 0, 22)
Logo.Parent = LeftPanel

local LogoGlow = Instance.new("ImageLabel")
LogoGlow.BackgroundTransparency = 1
LogoGlow.Image = "rbxassetid://5028857084"
LogoGlow.ImageColor3 = COLORS.Accent
LogoGlow.ImageTransparency = 0.7
LogoGlow.Size = UDim2.new(0, 120, 0, 120)
LogoGlow.Position = UDim2.new(0, -6, 0, -6)
LogoGlow.Parent = LeftPanel

local Brand = Instance.new("TextLabel")
Brand.BackgroundTransparency = 1
Brand.Text = "BANANA HUB"
Brand.Font = Enum.Font.GothamBlack
Brand.TextSize = 18
Brand.TextColor3 = COLORS.Text
Brand.TextXAlignment = Enum.TextXAlignment.Left
Brand.Position = UDim2.new(0, 24, 0, 86)
Brand.Size = UDim2.new(1, -48, 0, 22)
Brand.Parent = LeftPanel

local Tagline = Instance.new("TextLabel")
Tagline.BackgroundTransparency = 1
Tagline.Text = "Premium features, fast access."
Tagline.Font = Enum.Font.GothamMedium
Tagline.TextSize = 11
Tagline.TextColor3 = COLORS.Muted
Tagline.TextXAlignment = Enum.TextXAlignment.Left
Tagline.Position = UDim2.new(0, 24, 0, 110)
Tagline.Size = UDim2.new(1, -48, 0, 18)
Tagline.Parent = LeftPanel

local Features = Instance.new("Frame")
Features.BackgroundTransparency = 1
Features.Position = UDim2.new(0, 24, 0, 150)
Features.Size = UDim2.new(1, -48, 1, -180)
Features.Parent = LeftPanel

local function featureLine(text, y)
    local dot = Instance.new("Frame")
    dot.BackgroundColor3 = COLORS.Accent
    dot.Size = UDim2.new(0, 6, 0, 6)
    dot.Position = UDim2.new(0, 0, 0, y + 6)
    dot.Parent = Features
    createCorner(dot, 999)

    local label = Instance.new("TextLabel")
    label.BackgroundTransparency = 1
    label.Text = text
    label.Font = Enum.Font.GothamMedium
    label.TextSize = 11
    label.TextColor3 = COLORS.Muted
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Position = UDim2.new(0, 14, 0, y)
    label.Size = UDim2.new(1, -14, 0, 18)
    label.Parent = Features
end

featureLine("Instant verification", 0)
featureLine("Cloud updates", 22)
featureLine("Secure auth", 44)
featureLine("Fast support", 66)

-- Right login panel
local RightPanel = Instance.new("Frame")
RightPanel.Name = "RightPanel"
RightPanel.BackgroundTransparency = 1
RightPanel.Size = UDim2.new(1, -260, 1, -3)
RightPanel.Position = UDim2.new(0, 260, 0, 3)
RightPanel.Parent = Card

local Header = Instance.new("Frame")
Header.BackgroundTransparency = 1
Header.Size = UDim2.new(1, -48, 0, 70)
Header.Position = UDim2.new(0, 24, 0, 18)
Header.Parent = RightPanel

local Title = Instance.new("TextLabel")
Title.BackgroundTransparency = 1
Title.Text = "Welcome back"
Title.Font = Enum.Font.GothamBlack
Title.TextSize = 22
Title.TextColor3 = COLORS.Text
Title.TextXAlignment = Enum.TextXAlignment.Left
Title.Size = UDim2.new(1, 0, 0, 28)
Title.Parent = Header

local Subtitle = Instance.new("TextLabel")
Subtitle.BackgroundTransparency = 1
Subtitle.Text = "Enter your Discord ID and license key"
Subtitle.Font = Enum.Font.GothamMedium
Subtitle.TextSize = 12
Subtitle.TextColor3 = COLORS.Muted
Subtitle.TextXAlignment = Enum.TextXAlignment.Left
Subtitle.Position = UDim2.new(0, 0, 0, 30)
Subtitle.Size = UDim2.new(1, 0, 0, 20)
Subtitle.Parent = Header

-- Status badge
local StatusBadge = Instance.new("Frame")
StatusBadge.BackgroundColor3 = COLORS.PanelHi
StatusBadge.Position = UDim2.new(1, -160, 0, 18)
StatusBadge.Size = UDim2.new(0, 136, 0, 24)
StatusBadge.Parent = RightPanel
createCorner(StatusBadge, 999)
createStroke(StatusBadge, COLORS.Border, 1, 0.4)

local StatusDot = Instance.new("Frame")
StatusDot.BackgroundColor3 = COLORS.Muted
StatusDot.Size = UDim2.new(0, 8, 0, 8)
StatusDot.Position = UDim2.new(0, 10, 0.5, -4)
StatusDot.Parent = StatusBadge
createCorner(StatusDot, 999)

local StatusText = Instance.new("TextLabel")
StatusText.BackgroundTransparency = 1
StatusText.Text = "Checking..."
StatusText.Font = Enum.Font.GothamMedium
StatusText.TextSize = 10
StatusText.TextColor3 = COLORS.Muted
StatusText.TextXAlignment = Enum.TextXAlignment.Left
StatusText.Position = UDim2.new(0, 24, 0, 0)
StatusText.Size = UDim2.new(1, -28, 1, 0)
StatusText.Parent = StatusBadge

local Form = Instance.new("Frame")
Form.BackgroundTransparency = 1
Form.Position = UDim2.new(0, 24, 0, 110)
Form.Size = UDim2.new(1, -48, 0, 190)
Form.Parent = RightPanel

local function inputRow(labelText, placeholder, y)
    local container = Instance.new("Frame")
    container.BackgroundColor3 = COLORS.PanelHi
    container.Position = UDim2.new(0, 0, 0, y)
    container.Size = UDim2.new(1, 0, 0, 52)
    container.Parent = Form
    createCorner(container, 12)
    createStroke(container, COLORS.Border, 1, 0.5)

    local label = Instance.new("TextLabel")
    label.BackgroundTransparency = 1
    label.Text = labelText
    label.Font = Enum.Font.GothamBold
    label.TextSize = 10
    label.TextColor3 = COLORS.Muted
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Position = UDim2.new(0, 14, 0, -18)
    label.Size = UDim2.new(1, -28, 0, 16)
    label.Parent = container

    local input = Instance.new("TextBox")
    input.BackgroundTransparency = 1
    input.Text = ""
    input.PlaceholderText = placeholder
    input.PlaceholderColor3 = Color3.fromHex("#6b7280")
    input.Font = Enum.Font.GothamMedium
    input.TextSize = 13
    input.TextColor3 = COLORS.Text
    input.TextXAlignment = Enum.TextXAlignment.Left
    input.ClearTextOnFocus = false
    input.Position = UDim2.new(0, 14, 0, 0)
    input.Size = UDim2.new(1, -28, 1, 0)
    input.Parent = container

    input.Focused:Connect(function()
        TweenService:Create(container, TweenInfo.new(0.15), {BackgroundColor3 = Color3.fromHex("#1f2534")}):Play()
    end)
    input.FocusLost:Connect(function()
        TweenService:Create(container, TweenInfo.new(0.15), {BackgroundColor3 = COLORS.PanelHi}):Play()
    end)

    return input
end

local UserIDInput = inputRow("DISCORD ID", "Enter your Discord ID", 0)
local KeyInput = inputRow("LICENSE KEY", "BANANA-XXX-XXX-XXX", 76)

local LoginBtn = Instance.new("TextButton")
LoginBtn.BackgroundColor3 = COLORS.Accent
LoginBtn.Position = UDim2.new(0, 0, 0, 140)
LoginBtn.Size = UDim2.new(1, 0, 0, 48)
LoginBtn.Font = Enum.Font.GothamBold
LoginBtn.Text = "AUTHENTICATE"
LoginBtn.TextSize = 13
LoginBtn.TextColor3 = Color3.new(0, 0, 0)
LoginBtn.AutoButtonColor = false
LoginBtn.Parent = Form
createCorner(LoginBtn, 12)
createGradient(LoginBtn, COLORS.Accent, COLORS.Accent2, 0)

LoginBtn.MouseEnter:Connect(function()
    TweenService:Create(LoginBtn, TweenInfo.new(0.12), {Size = UDim2.new(1, 2, 0, 50)}):Play()
end)
LoginBtn.MouseLeave:Connect(function()
    TweenService:Create(LoginBtn, TweenInfo.new(0.12), {Size = UDim2.new(1, 0, 0, 48)}):Play()
end)

local Status = Instance.new("TextLabel")
Status.BackgroundTransparency = 1
Status.Position = UDim2.new(0, 24, 1, -30)
Status.Size = UDim2.new(1, -48, 0, 20)
Status.Font = Enum.Font.GothamMedium
Status.Text = ""
Status.TextColor3 = COLORS.Error
Status.TextSize = 11
Status.TextXAlignment = Enum.TextXAlignment.Left
Status.Parent = RightPanel

local Foot = Instance.new("TextLabel")
Foot.BackgroundTransparency = 1
Foot.Position = UDim2.new(0, 24, 1, -10)
Foot.Size = UDim2.new(1, -48, 0, 18)
Foot.Font = Enum.Font.Gotham
Foot.Text = "Secured • v4.2"
Foot.TextColor3 = COLORS.Muted
Foot.TextSize = 10
Foot.TextXAlignment = Enum.TextXAlignment.Left
Foot.Parent = RightPanel

-- Loading screen
local Loading = Instance.new("Frame")
Loading.Name = "Loading"
Loading.BackgroundTransparency = 0
Loading.BackgroundColor3 = COLORS.Bg
Loading.Size = UDim2.new(1, 0, 1, 0)
Loading.ZIndex = 50
Loading.Parent = Root

local LoadingCard = Instance.new("Frame")
LoadingCard.AnchorPoint = Vector2.new(0.5, 0.5)
LoadingCard.Position = UDim2.new(0.5, 0, 0.5, 0)
LoadingCard.Size = UDim2.new(0, 420, 0, 220)
LoadingCard.BackgroundColor3 = COLORS.Panel
LoadingCard.ZIndex = 51
LoadingCard.Parent = Loading
createCorner(LoadingCard, 18)
createStroke(LoadingCard, COLORS.Border, 1, 0.4)

local LoadingTitle = Instance.new("TextLabel")
LoadingTitle.BackgroundTransparency = 1
LoadingTitle.Text = "Loading Banana Hub"
LoadingTitle.Font = Enum.Font.GothamBlack
LoadingTitle.TextSize = 18
LoadingTitle.TextColor3 = COLORS.Text
LoadingTitle.Size = UDim2.new(1, -40, 0, 28)
LoadingTitle.Position = UDim2.new(0, 20, 0, 26)
LoadingTitle.Parent = LoadingCard

local LoadingSub = Instance.new("TextLabel")
LoadingSub.BackgroundTransparency = 1
LoadingSub.Text = "Preparing interface..."
LoadingSub.Font = Enum.Font.GothamMedium
LoadingSub.TextSize = 11
LoadingSub.TextColor3 = COLORS.Muted
LoadingSub.Position = UDim2.new(0, 20, 0, 52)
LoadingSub.Size = UDim2.new(1, -40, 0, 20)
LoadingSub.Parent = LoadingCard

local Bar = Instance.new("Frame")
Bar.BackgroundColor3 = COLORS.PanelHi
Bar.Position = UDim2.new(0, 20, 0, 120)
Bar.Size = UDim2.new(1, -40, 0, 8)
Bar.Parent = LoadingCard
createCorner(Bar, 6)
createStroke(Bar, COLORS.Border, 1, 0.5)

local BarFill = Instance.new("Frame")
BarFill.BackgroundColor3 = COLORS.Accent
BarFill.Size = UDim2.new(0, 0, 1, 0)
BarFill.Parent = Bar
createCorner(BarFill, 6)
createGradient(BarFill, COLORS.Accent, COLORS.Accent2, 0)

local Percent = Instance.new("TextLabel")
Percent.BackgroundTransparency = 1
Percent.Text = "0%"
Percent.Font = Enum.Font.GothamBold
Percent.TextSize = 11
Percent.TextColor3 = COLORS.Muted
Percent.Position = UDim2.new(0, 20, 0, 140)
Percent.Size = UDim2.new(0, 60, 0, 18)
Percent.Parent = LoadingCard

local function notify(msg, ok)
    Status.Text = msg
    Status.TextColor3 = ok and COLORS.Success or COLORS.Error
end

local function setButtonLoading(loading)
    if loading then
        LoginBtn.Text = "WORKING..."
        LoginBtn.Active = false
    else
        LoginBtn.Text = "AUTHENTICATE"
        LoginBtn.Active = true
    end
end

local function handleLogin()
    local uid = UserIDInput.Text
    local key = KeyInput.Text

    if uid == "" or key == "" then
        notify("ERROR: Fill in all fields", false)
        return
    end

    local apiUrl = resolveApiUrl()
    if not apiUrl then
        notify("ERROR: API URL not configured", false)
        return
    end

    notify("Authenticating...", true)
    setButtonLoading(true)

    local query = "user_id=" .. HttpService:UrlEncode(uid) .. "&key=" .. HttpService:UrlEncode(key)
    local ok, dataOrErr = requestJson("GET", apiUrl .. "/api/verify?" .. query)

    if not ok then
        local payload = HttpService:JSONEncode({uid = uid, user_id = uid, key = key})
        ok, dataOrErr = requestJson("POST", apiUrl .. "/api/auth", payload)
    end

    if ok then
        local data = dataOrErr
        local successFlag = data.success == true or data.authenticated == true or data.valid == true
        if successFlag then
            notify("Access Granted", true)
            TweenService:Create(LoginBtn, TweenInfo.new(0.2), {BackgroundColor3 = COLORS.Success}):Play()
            setButtonLoading(false)
            task.wait(0.6)
            TweenService:Create(blur, TweenInfo.new(0.35), {Size = 0}):Play()
            TweenService:Create(Card, TweenInfo.new(0.35, Enum.EasingStyle.Quad, Enum.EasingDirection.In), {
                Size = UDim2.new(0, 0, 0, 0),
                BackgroundTransparency = 1
            }):Play()
            task.wait(0.4)
            ScreenGui:Destroy()
            blur:Destroy()
            return
        end

        local errMsg = data.error or data.message or data.reason or "Invalid credentials"
        notify("ERROR: " .. tostring(errMsg), false)
    else
        local errLabel = tostring(dataOrErr or "")
        local msg = "ERROR: Connection failed"
        if errLabel ~= "" then
            msg = msg .. " (" .. errLabel .. ")"
        end
        notify(msg, false)
    end

    setButtonLoading(false)
end

LoginBtn.MouseButton1Click:Connect(handleLogin)

-- Status ping
local function updateStatus()
    local apiUrl = resolveApiUrl()
    if not apiUrl then
        StatusDot.BackgroundColor3 = COLORS.Error
        StatusText.Text = "API not set"
        StatusText.TextColor3 = COLORS.Error
        return
    end

    local ok = select(1, requestJson("GET", apiUrl .. "/api/status"))
    if ok then
        StatusDot.BackgroundColor3 = COLORS.Success
        StatusText.Text = "Online"
        StatusText.TextColor3 = COLORS.Success
    else
        StatusDot.BackgroundColor3 = COLORS.Error
        StatusText.Text = "Offline"
        StatusText.TextColor3 = COLORS.Error
    end
end

-- Loading sequence
local function endLoading()
    if not Loading.Visible then
        return
    end

    TweenService:Create(Loading, TweenInfo.new(0.25), {BackgroundTransparency = 1}):Play()
    TweenService:Create(LoadingCard, TweenInfo.new(0.25, Enum.EasingStyle.Quad, Enum.EasingDirection.In), {Size = UDim2.new(0, 0, 0, 0)}):Play()
    task.wait(0.3)
    Loading.Visible = false

    Card.Size = UDim2.new(0, 0, 0, 0)
    TweenService:Create(Card, TweenInfo.new(0.45, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {
        Size = UDim2.new(0, 720, 0, 380)
    }):Play()
end

local function runLoading()
    TweenService:Create(blur, TweenInfo.new(0.2), {Size = 0}):Play()
    for i = 1, 5 do
        local p = i / 5
        TweenService:Create(BarFill, TweenInfo.new(0.35, Enum.EasingStyle.Quad), {Size = UDim2.new(p, 0, 1, 0)}):Play()
        Percent.Text = math.floor(p * 100) .. "%"
        task.wait(0.4)
    end

    -- Default to offline, then try a live ping without blocking UI
    StatusDot.BackgroundColor3 = COLORS.Error
    StatusText.Text = "Offline"
    StatusText.TextColor3 = COLORS.Error
    task.spawn(function()
        pcall(updateStatus)
    end)
    endLoading()
end

-- Animated logo pulse
task.spawn(function()
    while ScreenGui.Parent do
        TweenService:Create(Logo, TweenInfo.new(1.2, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {Rotation = 8}):Play()
        TweenService:Create(LogoGlow, TweenInfo.new(1.2, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {ImageTransparency = 0.6}):Play()
        task.wait(1.2)
        TweenService:Create(Logo, TweenInfo.new(1.2, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {Rotation = -8}):Play()
        TweenService:Create(LogoGlow, TweenInfo.new(1.2, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut), {ImageTransparency = 0.75}):Play()
        task.wait(1.2)
    end
end)

-- Drag
local dragging = false
local dragStart, startPos
Card.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = true
        dragStart = input.Position
        startPos = Card.Position
    end
end)
Card.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = false
    end
end)
UserInputService.InputChanged:Connect(function(input)
    if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
        local delta = input.Position - dragStart
        Card.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
    end
end)

-- Start
task.delay(3, function()
    if Loading.Visible then
        endLoading()
    end
end)
runLoading()
