-- Banana Hub Platinum Loader
-- Premium Roblox Loader Script

local HttpService = game:GetService("HttpService")
local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")

local player = Players.LocalPlayer
local mouse = player:GetMouse()

-- Configuration (Injected by server or default)
local API_URL = "[[API_URL]]" -- Server will replace this placeholder

-- UI Constants
local COLORS = {
    Background = Color3.fromHex("#09090b"),
    Glass = Color3.fromHex("#141416"),
    Accent = Color3.fromHex("#FACC15"),
    Text = Color3.fromHex("#FFFFFF"),
    TextDim = Color3.fromHex("#A1A1AA"),
    Error = Color3.fromHex("#EF4444"),
    Success = Color3.fromHex("#22C55E")
}

-- Create UI
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "BananaHubLoader"
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- Try to put in CoreGui if possible, otherwise PlayerGui
local success, err = pcall(function()
    ScreenGui.Parent = CoreGui
end)
if not success then
    ScreenGui.Parent = player:WaitForChild("PlayerGui")
end

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

local function createShadow(parent)
    local shadow = Instance.new("ImageLabel")
    shadow.Name = "Shadow"
    shadow.AnchorPoint = Vector2.new(0.5, 0.5)
    shadow.BackgroundTransparency = 1
    shadow.Position = UDim2.new(0.5, 0, 0.5, 0)
    shadow.Size = UDim2.new(1, 40, 1, 40)
    shadow.ZIndex = math.max(1, parent.ZIndex - 1)
    shadow.Image = "rbxassetid://6015667343"
    shadow.ImageColor3 = Color3.new(0, 0, 0)
    shadow.ImageTransparency = 0.5
    shadow.ScaleType = Enum.ScaleType.Slice
    shadow.SliceCenter = Rect.new(49, 49, 450, 450)
    shadow.Parent = parent
    return shadow
end

-- Main Container
local MainFrame = Instance.new("Frame")
MainFrame.Name = "MainFrame"
MainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
MainFrame.BackgroundColor3 = COLORS.Background
MainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
MainFrame.Size = UDim2.new(0, 400, 0, 320)
MainFrame.ClipsDescendants = true
MainFrame.Parent = ScreenGui

createCorner(MainFrame, 20)
createStroke(MainFrame, COLORS.Accent, 1, 0.8)
createShadow(MainFrame)

-- Dragging Logic
local dragging, dragInput, dragStart, startPos
MainFrame.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = true
        dragStart = input.Position
        startPos = MainFrame.Position
    end
end)

MainFrame.InputChanged:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseMovement then
        dragInput = input
    end
end)

game:GetService("UserInputService").InputChanged:Connect(function(input)
    if input == dragInput and dragging then
        local delta = input.Position - dragStart
        MainFrame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
    end
end)

game:GetService("UserInputService").InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = false
    end
end)

-- --- LOADING SCREEN ---
local LoadingFrame = Instance.new("Frame")
LoadingFrame.Name = "LoadingFrame"
LoadingFrame.BackgroundTransparency = 1
LoadingFrame.Size = UDim2.new(1, 0, 1, 0)
LoadingFrame.ZIndex = 10
LoadingFrame.Parent = MainFrame

local Logo = Instance.new("ImageLabel")
Logo.Name = "Logo"
Logo.AnchorPoint = Vector2.new(0.5, 0.5)
Logo.BackgroundTransparency = 1
Logo.Position = UDim2.new(0.5, 0, 0.4, 0)
Logo.Size = UDim2.new(0, 80, 0, 80)
Logo.Image = "rbxassetid://13192004240" -- Generic banana icon
Logo.ImageColor3 = COLORS.Accent
Logo.Parent = LoadingFrame

local LoadingText = Instance.new("TextLabel")
LoadingText.Name = "LoadingText"
LoadingText.AnchorPoint = Vector2.new(0.5, 0.5)
LoadingText.BackgroundTransparency = 1
LoadingText.Position = UDim2.new(0.5, 0, 0.65, 0)
LoadingText.Size = UDim2.new(1, 0, 0, 30)
LoadingText.Font = Enum.Font.GothamBold
LoadingText.Text = "BANANA HUB"
LoadingText.TextColor3 = COLORS.Text
LoadingText.TextSize = 24
LoadingText.Parent = LoadingFrame

local LoadingProgress = Instance.new("Frame")
LoadingProgress.Name = "ProgressBar"
LoadingProgress.AnchorPoint = Vector2.new(0.5, 0.5)
LoadingProgress.BackgroundColor3 = COLORS.Glass
LoadingProgress.Position = UDim2.new(0.5, 0, 0.75, 0)
LoadingProgress.Size = UDim2.new(0, 200, 0, 4)
LoadingProgress.Parent = LoadingFrame
createCorner(LoadingProgress, 2)

local Fill = Instance.new("Frame")
Fill.Name = "Fill"
Fill.BackgroundColor3 = COLORS.Accent
Fill.Size = UDim2.new(0, 0, 1, 0)
Fill.Parent = LoadingProgress
createCorner(Fill, 2)

-- --- LOGIN SCREEN ---
local LoginFrame = Instance.new("Frame")
LoginFrame.Name = "LoginFrame"
LoginFrame.BackgroundTransparency = 1
LoginFrame.Size = UDim2.new(1, 0, 1, 0)
LoginFrame.Visible = false
LoginFrame.Parent = MainFrame

local Header = Instance.new("Frame")
Header.Name = "Header"
Header.BackgroundTransparency = 1
Header.Size = UDim2.new(1, 0, 0, 80)
Header.Parent = LoginFrame

local Title = Instance.new("TextLabel")
Title.Name = "Title"
Title.BackgroundTransparency = 1
Title.Position = UDim2.new(0, 30, 0, 30)
Title.Size = UDim2.new(1, -60, 0, 30)
Title.Font = Enum.Font.GothamBold
Title.Text = "Welcome to Platinum"
Title.TextColor3 = COLORS.Text
Title.TextSize = 22
Title.TextXAlignment = Enum.TextXAlignment.Left
Title.Parent = Header

local Desc = Instance.new("TextLabel")
Desc.Name = "Desc"
Desc.BackgroundTransparency = 1
Desc.Position = UDim2.new(0, 30, 0, 55)
Desc.Size = UDim2.new(1, -60, 0, 20)
Desc.Font = Enum.Font.Gotham
Desc.Text = "Authenticate to unlock premium features."
Desc.TextColor3 = COLORS.TextDim
Desc.TextSize = 13
Desc.TextXAlignment = Enum.TextXAlignment.Left
Desc.Parent = Header

-- Input Fields
local function createInput(name, placeholder, position)
    local container = Instance.new("Frame")
    container.Name = name .. "Container"
    container.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    container.Position = position
    container.Size = UDim2.new(1, -60, 0, 48)
    container.Parent = LoginFrame
    
    createCorner(container, 10)
    createStroke(container, COLORS.TextDim, 1, 0.9)
    
    local label = Instance.new("TextLabel")
    label.Name = "Label"
    label.BackgroundTransparency = 1
    label.Position = UDim2.new(0, 0, 0, -20)
    label.Size = UDim2.new(1, 0, 0, 20)
    label.Font = Enum.Font.GothamBold
    label.Text = name:upper()
    label.TextColor3 = COLORS.TextDim
    label.TextSize = 10
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Parent = container

    local input = Instance.new("TextBox")
    input.Name = "Input"
    input.BackgroundTransparency = 1
    input.Position = UDim2.new(0, 15, 0, 0)
    input.Size = UDim2.new(1, -30, 1, 0)
    input.Font = Enum.Font.Gotham
    input.PlaceholderText = placeholder
    input.PlaceholderColor3 = Color3.fromRGB(60, 60, 60)
    input.Text = ""
    input.TextColor3 = COLORS.Text
    input.TextSize = 14
    input.TextXAlignment = Enum.TextXAlignment.Left
    input.ClearTextOnFocus = false
    input.Parent = container
    
    input.Focused:Connect(function()
        TweenService:Create(container.UIStroke, TweenInfo.new(0.3), {Color = COLORS.Accent, Transparency = 0.5}):Play()
    end)
    
    input.FocusLost:Connect(function()
        TweenService:Create(container.UIStroke, TweenInfo.new(0.3), {Color = COLORS.TextDim, Transparency = 0.9}):Play()
    end)
    
    return input
end

local UserIDInput = createInput("Discord ID", "Enter your User ID", UDim2.new(0, 30, 0, 110))
local KeyInput = createInput("License Key", "BANANA-XXXX-XXXX-XXXX", UDim2.new(0, 30, 0, 185))

-- Login Button
local LoginBtn = Instance.new("TextButton")
LoginBtn.Name = "LoginBtn"
LoginBtn.BackgroundColor3 = COLORS.Accent
LoginBtn.Position = UDim2.new(0, 30, 0, 250)
LoginBtn.Size = UDim2.new(1, -60, 0, 48)
LoginBtn.Font = Enum.Font.GothamBold
LoginBtn.Text = "AUTHENTICATE"
LoginBtn.TextColor3 = Color3.new(0, 0, 0)
LoginBtn.TextSize = 14
LoginBtn.AutoButtonColor = false
LoginBtn.Parent = LoginFrame

createCorner(LoginBtn, 10)

local Status = Instance.new("TextLabel")
Status.Name = "Status"
Status.AnchorPoint = Vector2.new(0.5, 0)
Status.BackgroundTransparency = 1
Status.Position = UDim2.new(0.5, 0, 0, 302)
Status.Size = UDim2.new(1, -60, 0, 20)
Status.Font = Enum.Font.Gotham
Status.Text = ""
Status.TextColor3 = COLORS.Error
Status.TextSize = 11
Status.Parent = LoginFrame

-- --- LOGIC ---

local function notify(msg, success)
    Status.Text = msg
    Status.TextColor3 = success and COLORS.Success or COLORS.Error
end

local function handleLogin()
    local uid = UserIDInput.Text
    local key = KeyInput.Text
    
    if uid == "" or key == "" then
        notify("❌ Please fill all fields.", false)
        return
    end
    
    notify("⏳ Authenticating...", true)
    LoginBtn.Text = "VERIFYING..."
    LoginBtn.Active = false
    
    -- API CALL
    local success, response = pcall(function()
        -- Note: Custom executors usually provide a more robust 'request' function, 
        -- but game:HttpGet is standard for simple GETs.
        return game:HttpGet(string.format("%s/api/verify?user_id=%s&key=%s", API_URL, uid, key))
    end)
    
    if success then
        local data
        local decode_ok, err = pcall(function()
            data = HttpService:JSONDecode(response)
        end)
        
        if decode_ok and data.success then
            notify("✅ Access Granted! Initializing...", true)
            task.wait(1.5)
            
            -- Fade Out and Destroy
            local fade = TweenService:Create(MainFrame, TweenInfo.new(0.7, Enum.EasingStyle.Quart, Enum.EasingDirection.In), {
                Size = UDim2.new(0, 0, 0, 0),
                BackgroundTransparency = 1
            })
            fade:Play()
            fade.Completed:Wait()
            ScreenGui:Destroy()
            
            print("[Banana Hub] Loader finished successfully.")
            -- Here you would load the actual script features
        else
            notify("❌ " .. (data and data.error or "Invalid Credentials"), false)
            LoginBtn.Text = "AUTHENTICATE"
            LoginBtn.Active = true
        end
    else
        notify("❌ Connection failed (Server Offline)", false)
        LoginBtn.Text = "AUTHENTICATE"
        LoginBtn.Active = true
    end
end

-- Hover Effects
LoginBtn.MouseEnter:Connect(function()
    TweenService:Create(LoginBtn, TweenInfo.new(0.3), {BackgroundColor3 = COLORS.Accent:Lerp(Color3.new(1,1,1), 0.15)}):Play()
end)

LoginBtn.MouseLeave:Connect(function()
    TweenService:Create(LoginBtn, TweenInfo.new(0.3), {BackgroundColor3 = COLORS.Accent}):Play()
end)

LoginBtn.MouseButton1Click:Connect(handleLogin)

-- Loading Animation
task.spawn(function()
    TweenService:Create(Fill, TweenInfo.new(2.5, Enum.EasingStyle.Quart), {Size = UDim2.new(1, 0, 1, 0)}):Play()
    task.wait(2.7)
    
    -- Transition
    local fadeOut = TweenService:Create(LoadingFrame, TweenInfo.new(0.5), {Position = UDim2.new(0, 0, -1, 0)})
    fadeOut:Play()
    fadeOut.Completed:Wait()
    
    LoadingFrame.Visible = false
    LoginFrame.Visible = true
    LoginFrame.Position = UDim2.new(0, 0, 1, 0)
    
    TweenService:Create(LoginFrame, TweenInfo.new(0.8, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {Position = UDim2.new(0, 0, 0, 0)}):Play()
end)
