# 🚪 TeleGate

**TeleGate** is a secure, invite-based **Telegram user management system** built with **Django** and **Telebot**.  
It provides a hierarchical structure of **Super Admins**, **Admins**, and **Users**, allowing full access control through expiring invite links.

---

## ✨ Features

- 🧩 **Role Hierarchy**
  - Super Admin, Admin, and User panels  
- 🔗 **Invite-Only Access**
  - Users can only activate their panel through a valid invite link  
- ⏳ **Expiring Links**
  - All invite links automatically expire after 10 minutes  
- ⚙️ **Panels Overview**
  - **User:** Enable/disable alerts, view account info, access support  
  - **Admin:** Generate invite & subscription links, view/delete user list  
  - **Super Admin:** Manage admins, emergency stop, generate admin links  

---

## 🧱 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | **Django** |
| Telegram Bot | **Telebot (PyTelegramBotAPI)** |
| Database | **SQLite** |

---

> 📘 For installation instructions, see [INSTALL.md](/INSTALL.md).