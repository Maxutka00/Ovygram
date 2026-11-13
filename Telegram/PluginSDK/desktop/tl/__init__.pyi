from .codec import (TLObject as TLObject, constructor as constructor,
                    decode as decode, encode as encode, response_type as response_type)

class account:
    class acceptAuthorization(TLObject):
        bot_id: int
        scope: str
        public_key: str
        value_hashes: list[TLObject]
        credentials: TLObject
        def __init__(self, *, bot_id: int, scope: str, public_key: str, value_hashes: list[TLObject], credentials: TLObject) -> None: ...

    class authorizationForm(TLObject):
        required_types: list[TLObject]
        values: list[TLObject]
        errors: list[TLObject]
        users: list[TLObject]
        privacy_policy_url: str | None
        def __init__(self, *, required_types: list[TLObject], values: list[TLObject], errors: list[TLObject], users: list[TLObject], privacy_policy_url: str | None = ...) -> None: ...

    class authorizations(TLObject):
        authorization_ttl_days: int
        authorizations: list[TLObject]
        def __init__(self, *, authorization_ttl_days: int, authorizations: list[TLObject]) -> None: ...

    class autoDownloadSettings(TLObject):
        low: TLObject
        medium: TLObject
        high: TLObject
        def __init__(self, *, low: TLObject, medium: TLObject, high: TLObject) -> None: ...

    class autoSaveSettings(TLObject):
        users_settings: TLObject
        chats_settings: TLObject
        broadcasts_settings: TLObject
        exceptions: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, users_settings: TLObject, chats_settings: TLObject, broadcasts_settings: TLObject, exceptions: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class businessChatLinks(TLObject):
        links: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, links: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class cancelPasswordEmail(TLObject):
        def __init__(self) -> None: ...

    class changeAuthorizationSettings(TLObject):
        confirmed: bool
        hash: int
        encrypted_requests_disabled: bool
        call_requests_disabled: bool
        def __init__(self, *, confirmed: bool = ..., hash: int, encrypted_requests_disabled: bool = ..., call_requests_disabled: bool = ...) -> None: ...

    class changePhone(TLObject):
        phone_number: str
        phone_code_hash: str
        phone_code: str
        def __init__(self, *, phone_number: str, phone_code_hash: str, phone_code: str) -> None: ...

    class chatThemes(TLObject):
        hash: int
        themes: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        next_offset: str | None
        def __init__(self, *, hash: int, themes: list[TLObject], chats: list[TLObject], users: list[TLObject], next_offset: str | None = ...) -> None: ...

    class chatThemesNotModified(TLObject):
        def __init__(self) -> None: ...

    class checkUsername(TLObject):
        username: str
        def __init__(self, *, username: str) -> None: ...

    class clearRecentEmojiStatuses(TLObject):
        def __init__(self) -> None: ...

    class confirmBotConnection(TLObject):
        bot_id: TLObject
        def __init__(self, *, bot_id: TLObject) -> None: ...

    class confirmPasswordEmail(TLObject):
        code: str
        def __init__(self, *, code: str) -> None: ...

    class confirmPhone(TLObject):
        phone_code_hash: str
        phone_code: str
        def __init__(self, *, phone_code_hash: str, phone_code: str) -> None: ...

    class connectedBots(TLObject):
        connected_bots: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, connected_bots: list[TLObject], users: list[TLObject]) -> None: ...

    class contentSettings(TLObject):
        sensitive_enabled: bool
        sensitive_can_change: bool
        def __init__(self, *, sensitive_enabled: bool = ..., sensitive_can_change: bool = ...) -> None: ...

    class createBusinessChatLink(TLObject):
        link: TLObject
        def __init__(self, *, link: TLObject) -> None: ...

    class createTheme(TLObject):
        slug: str
        title: str
        document: TLObject | None
        settings: list[TLObject] | None
        def __init__(self, *, slug: str, title: str, document: TLObject | None = ..., settings: list[TLObject] | None = ...) -> None: ...

    class declinePasswordReset(TLObject):
        def __init__(self) -> None: ...

    class deleteAccount(TLObject):
        reason: str
        password: TLObject | None
        def __init__(self, *, reason: str, password: TLObject | None = ...) -> None: ...

    class deleteAutoSaveExceptions(TLObject):
        def __init__(self) -> None: ...

    class deleteBusinessChatLink(TLObject):
        slug: str
        def __init__(self, *, slug: str) -> None: ...

    class deletePasskey(TLObject):
        id: str
        def __init__(self, *, id: str) -> None: ...

    class deleteSecureValue(TLObject):
        types: list[TLObject]
        def __init__(self, *, types: list[TLObject]) -> None: ...

    class deleteWebBrowserSettingsExceptions(TLObject):
        def __init__(self) -> None: ...

    class disablePeerConnectedBot(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class editBusinessChatLink(TLObject):
        slug: str
        link: TLObject
        def __init__(self, *, slug: str, link: TLObject) -> None: ...

    class emailVerified(TLObject):
        email: str
        def __init__(self, *, email: str) -> None: ...

    class emailVerifiedLogin(TLObject):
        email: str
        sent_code: TLObject
        def __init__(self, *, email: str, sent_code: TLObject) -> None: ...

    class emojiStatuses(TLObject):
        hash: int
        statuses: list[TLObject]
        def __init__(self, *, hash: int, statuses: list[TLObject]) -> None: ...

    class emojiStatusesNotModified(TLObject):
        def __init__(self) -> None: ...

    class finishTakeoutSession(TLObject):
        success: bool
        def __init__(self, *, success: bool = ...) -> None: ...

    class getAccountTTL(TLObject):
        def __init__(self) -> None: ...

    class getAllSecureValues(TLObject):
        def __init__(self) -> None: ...

    class getAuthorizationForm(TLObject):
        bot_id: int
        scope: str
        public_key: str
        def __init__(self, *, bot_id: int, scope: str, public_key: str) -> None: ...

    class getAuthorizations(TLObject):
        def __init__(self) -> None: ...

    class getAutoDownloadSettings(TLObject):
        def __init__(self) -> None: ...

    class getAutoSaveSettings(TLObject):
        def __init__(self) -> None: ...

    class getBotBusinessConnection(TLObject):
        connection_id: str
        def __init__(self, *, connection_id: str) -> None: ...

    class getBusinessChatLinks(TLObject):
        def __init__(self) -> None: ...

    class getChannelDefaultEmojiStatuses(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getChannelRestrictedStatusEmojis(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getChatThemes(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getCollectibleEmojiStatuses(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getConnectedBots(TLObject):
        def __init__(self) -> None: ...

    class getContactSignUpNotification(TLObject):
        def __init__(self) -> None: ...

    class getContentSettings(TLObject):
        def __init__(self) -> None: ...

    class getDefaultBackgroundEmojis(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getDefaultEmojiStatuses(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getDefaultGroupPhotoEmojis(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getDefaultProfilePhotoEmojis(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getGlobalPrivacySettings(TLObject):
        def __init__(self) -> None: ...

    class getMultiWallPapers(TLObject):
        wallpapers: list[TLObject]
        def __init__(self, *, wallpapers: list[TLObject]) -> None: ...

    class getNotifyExceptions(TLObject):
        compare_sound: bool
        compare_stories: bool
        peer: TLObject | None
        def __init__(self, *, compare_sound: bool = ..., compare_stories: bool = ..., peer: TLObject | None = ...) -> None: ...

    class getNotifySettings(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getPaidMessagesRevenue(TLObject):
        parent_peer: TLObject | None
        user_id: TLObject
        def __init__(self, *, parent_peer: TLObject | None = ..., user_id: TLObject) -> None: ...

    class getPasskeys(TLObject):
        def __init__(self) -> None: ...

    class getPassword(TLObject):
        def __init__(self) -> None: ...

    class getPasswordSettings(TLObject):
        password: TLObject
        def __init__(self, *, password: TLObject) -> None: ...

    class getPrivacy(TLObject):
        key: TLObject
        def __init__(self, *, key: TLObject) -> None: ...

    class getReactionsNotifySettings(TLObject):
        def __init__(self) -> None: ...

    class getRecentEmojiStatuses(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getSavedMusicIds(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getSavedRingtones(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getSecureValue(TLObject):
        types: list[TLObject]
        def __init__(self, *, types: list[TLObject]) -> None: ...

    class getTheme(TLObject):
        format: str
        theme: TLObject
        def __init__(self, *, format: str, theme: TLObject) -> None: ...

    class getThemes(TLObject):
        format: str
        hash: int
        def __init__(self, *, format: str, hash: int) -> None: ...

    class getTmpPassword(TLObject):
        password: TLObject
        period: int
        def __init__(self, *, password: TLObject, period: int) -> None: ...

    class getUniqueGiftChatThemes(TLObject):
        offset: str
        limit: int
        hash: int
        def __init__(self, *, offset: str, limit: int, hash: int) -> None: ...

    class getWallPaper(TLObject):
        wallpaper: TLObject
        def __init__(self, *, wallpaper: TLObject) -> None: ...

    class getWallPapers(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getWebAuthorizations(TLObject):
        def __init__(self) -> None: ...

    class getWebBrowserSettings(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class initPasskeyRegistration(TLObject):
        def __init__(self) -> None: ...

    class initTakeoutSession(TLObject):
        contacts: bool
        message_users: bool
        message_chats: bool
        message_megagroups: bool
        message_channels: bool
        files: bool
        file_max_size: int | None
        def __init__(self, *, contacts: bool = ..., message_users: bool = ..., message_chats: bool = ..., message_megagroups: bool = ..., message_channels: bool = ..., files: bool = ..., file_max_size: int | None = ...) -> None: ...

    class installTheme(TLObject):
        dark: bool
        theme: TLObject | None
        format: str | None
        base_theme: TLObject | None
        def __init__(self, *, dark: bool = ..., theme: TLObject | None = ..., format: str | None = ..., base_theme: TLObject | None = ...) -> None: ...

    class installWallPaper(TLObject):
        wallpaper: TLObject
        settings: TLObject
        def __init__(self, *, wallpaper: TLObject, settings: TLObject) -> None: ...

    class invalidateSignInCodes(TLObject):
        codes: list[str]
        def __init__(self, *, codes: list[str]) -> None: ...

    class paidMessagesRevenue(TLObject):
        stars_amount: int
        def __init__(self, *, stars_amount: int) -> None: ...

    class passkeyRegistrationOptions(TLObject):
        options: TLObject
        def __init__(self, *, options: TLObject) -> None: ...

    class passkeys(TLObject):
        passkeys: list[TLObject]
        def __init__(self, *, passkeys: list[TLObject]) -> None: ...

    class password(TLObject):
        has_recovery: bool
        has_secure_values: bool
        has_password: bool
        current_algo: TLObject | None
        srp_B: bytes | None
        srp_id: int | None
        hint: str | None
        email_unconfirmed_pattern: str | None
        new_algo: TLObject
        new_secure_algo: TLObject
        secure_random: bytes
        pending_reset_date: int | None
        login_email_pattern: str | None
        def __init__(self, *, has_recovery: bool = ..., has_secure_values: bool = ..., has_password: bool = ..., current_algo: TLObject | None = ..., srp_B: bytes | None = ..., srp_id: int | None = ..., hint: str | None = ..., email_unconfirmed_pattern: str | None = ..., new_algo: TLObject, new_secure_algo: TLObject, secure_random: bytes, pending_reset_date: int | None = ..., login_email_pattern: str | None = ...) -> None: ...

    class passwordInputSettings(TLObject):
        new_algo: TLObject | None
        new_password_hash: bytes | None
        hint: str | None
        email: str | None
        new_secure_settings: TLObject | None
        def __init__(self, *, new_algo: TLObject | None = ..., new_password_hash: bytes | None = ..., hint: str | None = ..., email: str | None = ..., new_secure_settings: TLObject | None = ...) -> None: ...

    class passwordSettings(TLObject):
        email: str | None
        secure_settings: TLObject | None
        def __init__(self, *, email: str | None = ..., secure_settings: TLObject | None = ...) -> None: ...

    class privacyRules(TLObject):
        rules: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, rules: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class registerDevice(TLObject):
        no_muted: bool
        token_type: int
        token: str
        app_sandbox: bool
        secret: bytes
        other_uids: list[int]
        def __init__(self, *, no_muted: bool = ..., token_type: int, token: str, app_sandbox: bool, secret: bytes, other_uids: list[int]) -> None: ...

    class registerPasskey(TLObject):
        credential: TLObject
        def __init__(self, *, credential: TLObject) -> None: ...

    class reorderUsernames(TLObject):
        order: list[str]
        def __init__(self, *, order: list[str]) -> None: ...

    class reportPeer(TLObject):
        peer: TLObject
        reason: TLObject
        message: str
        def __init__(self, *, peer: TLObject, reason: TLObject, message: str) -> None: ...

    class reportProfilePhoto(TLObject):
        peer: TLObject
        photo_id: TLObject
        reason: TLObject
        message: str
        def __init__(self, *, peer: TLObject, photo_id: TLObject, reason: TLObject, message: str) -> None: ...

    class resendPasswordEmail(TLObject):
        def __init__(self) -> None: ...

    class resetAuthorization(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class resetNotifySettings(TLObject):
        def __init__(self) -> None: ...

    class resetPassword(TLObject):
        def __init__(self) -> None: ...

    class resetPasswordFailedWait(TLObject):
        retry_date: int
        def __init__(self, *, retry_date: int) -> None: ...

    class resetPasswordOk(TLObject):
        def __init__(self) -> None: ...

    class resetPasswordRequestedWait(TLObject):
        until_date: int
        def __init__(self, *, until_date: int) -> None: ...

    class resetWallPapers(TLObject):
        def __init__(self) -> None: ...

    class resetWebAuthorization(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class resetWebAuthorizations(TLObject):
        def __init__(self) -> None: ...

    class resolveBusinessChatLink(TLObject):
        slug: str
        def __init__(self, *, slug: str) -> None: ...

    class resolvedBusinessChatLinks(TLObject):
        peer: TLObject
        message: str
        entities: list[TLObject] | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, peer: TLObject, message: str, entities: list[TLObject] | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class saveAutoDownloadSettings(TLObject):
        low: bool
        high: bool
        settings: TLObject
        def __init__(self, *, low: bool = ..., high: bool = ..., settings: TLObject) -> None: ...

    class saveAutoSaveSettings(TLObject):
        users: bool
        chats: bool
        broadcasts: bool
        peer: TLObject | None
        settings: TLObject
        def __init__(self, *, users: bool = ..., chats: bool = ..., broadcasts: bool = ..., peer: TLObject | None = ..., settings: TLObject) -> None: ...

    class saveMusic(TLObject):
        unsave: bool
        id: TLObject
        after_id: TLObject | None
        def __init__(self, *, unsave: bool = ..., id: TLObject, after_id: TLObject | None = ...) -> None: ...

    class saveRingtone(TLObject):
        id: TLObject
        unsave: bool
        def __init__(self, *, id: TLObject, unsave: bool) -> None: ...

    class saveSecureValue(TLObject):
        value: TLObject
        secure_secret_id: int
        def __init__(self, *, value: TLObject, secure_secret_id: int) -> None: ...

    class saveTheme(TLObject):
        theme: TLObject
        unsave: bool
        def __init__(self, *, theme: TLObject, unsave: bool) -> None: ...

    class saveWallPaper(TLObject):
        wallpaper: TLObject
        unsave: bool
        settings: TLObject
        def __init__(self, *, wallpaper: TLObject, unsave: bool, settings: TLObject) -> None: ...

    class savedMusicIds(TLObject):
        ids: list[int]
        def __init__(self, *, ids: list[int]) -> None: ...

    class savedMusicIdsNotModified(TLObject):
        def __init__(self) -> None: ...

    class savedRingtone(TLObject):
        def __init__(self) -> None: ...

    class savedRingtoneConverted(TLObject):
        document: TLObject
        def __init__(self, *, document: TLObject) -> None: ...

    class savedRingtones(TLObject):
        hash: int
        ringtones: list[TLObject]
        def __init__(self, *, hash: int, ringtones: list[TLObject]) -> None: ...

    class savedRingtonesNotModified(TLObject):
        def __init__(self) -> None: ...

    class sendChangePhoneCode(TLObject):
        phone_number: str
        settings: TLObject
        def __init__(self, *, phone_number: str, settings: TLObject) -> None: ...

    class sendConfirmPhoneCode(TLObject):
        hash: str
        settings: TLObject
        def __init__(self, *, hash: str, settings: TLObject) -> None: ...

    class sendVerifyEmailCode(TLObject):
        purpose: TLObject
        email: str
        def __init__(self, *, purpose: TLObject, email: str) -> None: ...

    class sendVerifyPhoneCode(TLObject):
        phone_number: str
        settings: TLObject
        def __init__(self, *, phone_number: str, settings: TLObject) -> None: ...

    class sentEmailCode(TLObject):
        email_pattern: str
        length: int
        def __init__(self, *, email_pattern: str, length: int) -> None: ...

    class setAccountTTL(TLObject):
        ttl: TLObject
        def __init__(self, *, ttl: TLObject) -> None: ...

    class setAuthorizationTTL(TLObject):
        authorization_ttl_days: int
        def __init__(self, *, authorization_ttl_days: int) -> None: ...

    class setContactSignUpNotification(TLObject):
        silent: bool
        def __init__(self, *, silent: bool) -> None: ...

    class setContentSettings(TLObject):
        sensitive_enabled: bool
        def __init__(self, *, sensitive_enabled: bool = ...) -> None: ...

    class setGlobalPrivacySettings(TLObject):
        settings: TLObject
        def __init__(self, *, settings: TLObject) -> None: ...

    class setMainProfileTab(TLObject):
        tab: TLObject
        def __init__(self, *, tab: TLObject) -> None: ...

    class setPrivacy(TLObject):
        key: TLObject
        rules: list[TLObject]
        def __init__(self, *, key: TLObject, rules: list[TLObject]) -> None: ...

    class setReactionsNotifySettings(TLObject):
        settings: TLObject
        def __init__(self, *, settings: TLObject) -> None: ...

    class takeout(TLObject):
        id: int
        def __init__(self, *, id: int) -> None: ...

    class themes(TLObject):
        hash: int
        themes: list[TLObject]
        def __init__(self, *, hash: int, themes: list[TLObject]) -> None: ...

    class themesNotModified(TLObject):
        def __init__(self) -> None: ...

    class tmpPassword(TLObject):
        tmp_password: bytes
        valid_until: int
        def __init__(self, *, tmp_password: bytes, valid_until: int) -> None: ...

    class toggleConnectedBotPaused(TLObject):
        peer: TLObject
        paused: bool
        def __init__(self, *, peer: TLObject, paused: bool) -> None: ...

    class toggleNoPaidMessagesException(TLObject):
        refund_charged: bool
        require_payment: bool
        parent_peer: TLObject | None
        user_id: TLObject
        def __init__(self, *, refund_charged: bool = ..., require_payment: bool = ..., parent_peer: TLObject | None = ..., user_id: TLObject) -> None: ...

    class toggleSponsoredMessages(TLObject):
        enabled: bool
        def __init__(self, *, enabled: bool) -> None: ...

    class toggleUsername(TLObject):
        username: str
        active: bool
        def __init__(self, *, username: str, active: bool) -> None: ...

    class toggleWebBrowserSettingsException(TLObject):
        delete: bool
        open_external_browser: bool
        url: str
        def __init__(self, *, delete: bool = ..., open_external_browser: bool = ..., url: str) -> None: ...

    class unregisterDevice(TLObject):
        token_type: int
        token: str
        other_uids: list[int]
        def __init__(self, *, token_type: int, token: str, other_uids: list[int]) -> None: ...

    class updateBirthday(TLObject):
        birthday: TLObject | None
        def __init__(self, *, birthday: TLObject | None = ...) -> None: ...

    class updateBusinessAwayMessage(TLObject):
        message: TLObject | None
        def __init__(self, *, message: TLObject | None = ...) -> None: ...

    class updateBusinessGreetingMessage(TLObject):
        message: TLObject | None
        def __init__(self, *, message: TLObject | None = ...) -> None: ...

    class updateBusinessIntro(TLObject):
        intro: TLObject | None
        def __init__(self, *, intro: TLObject | None = ...) -> None: ...

    class updateBusinessLocation(TLObject):
        geo_point: TLObject | None
        address: str | None
        def __init__(self, *, geo_point: TLObject | None = ..., address: str | None = ...) -> None: ...

    class updateBusinessWorkHours(TLObject):
        business_work_hours: TLObject | None
        def __init__(self, *, business_work_hours: TLObject | None = ...) -> None: ...

    class updateColor(TLObject):
        for_profile: bool
        color: TLObject | None
        def __init__(self, *, for_profile: bool = ..., color: TLObject | None = ...) -> None: ...

    class updateConnectedBot(TLObject):
        deleted: bool
        rights: TLObject | None
        bot: TLObject
        recipients: TLObject
        def __init__(self, *, deleted: bool = ..., rights: TLObject | None = ..., bot: TLObject, recipients: TLObject) -> None: ...

    class updateDeviceLocked(TLObject):
        period: int
        def __init__(self, *, period: int) -> None: ...

    class updateEmojiStatus(TLObject):
        emoji_status: TLObject
        def __init__(self, *, emoji_status: TLObject) -> None: ...

    class updateNotifySettings(TLObject):
        peer: TLObject
        settings: TLObject
        def __init__(self, *, peer: TLObject, settings: TLObject) -> None: ...

    class updatePasswordSettings(TLObject):
        password: TLObject
        new_settings: TLObject
        def __init__(self, *, password: TLObject, new_settings: TLObject) -> None: ...

    class updatePersonalChannel(TLObject):
        channel: TLObject
        def __init__(self, *, channel: TLObject) -> None: ...

    class updateProfile(TLObject):
        first_name: str | None
        last_name: str | None
        about: str | None
        def __init__(self, *, first_name: str | None = ..., last_name: str | None = ..., about: str | None = ...) -> None: ...

    class updateStatus(TLObject):
        offline: bool
        def __init__(self, *, offline: bool) -> None: ...

    class updateTheme(TLObject):
        format: str
        theme: TLObject
        slug: str | None
        title: str | None
        document: TLObject | None
        settings: list[TLObject] | None
        def __init__(self, *, format: str, theme: TLObject, slug: str | None = ..., title: str | None = ..., document: TLObject | None = ..., settings: list[TLObject] | None = ...) -> None: ...

    class updateUsername(TLObject):
        username: str
        def __init__(self, *, username: str) -> None: ...

    class updateWebBrowserSettings(TLObject):
        open_external_browser: bool
        display_close_button: bool
        def __init__(self, *, open_external_browser: bool = ..., display_close_button: bool = ...) -> None: ...

    class uploadRingtone(TLObject):
        file: TLObject
        file_name: str
        mime_type: str
        def __init__(self, *, file: TLObject, file_name: str, mime_type: str) -> None: ...

    class uploadTheme(TLObject):
        file: TLObject
        thumb: TLObject | None
        file_name: str
        mime_type: str
        def __init__(self, *, file: TLObject, thumb: TLObject | None = ..., file_name: str, mime_type: str) -> None: ...

    class uploadWallPaper(TLObject):
        for_chat: bool
        file: TLObject
        mime_type: str
        settings: TLObject
        def __init__(self, *, for_chat: bool = ..., file: TLObject, mime_type: str, settings: TLObject) -> None: ...

    class verifyEmail(TLObject):
        purpose: TLObject
        verification: TLObject
        def __init__(self, *, purpose: TLObject, verification: TLObject) -> None: ...

    class verifyPhone(TLObject):
        phone_number: str
        phone_code_hash: str
        phone_code: str
        def __init__(self, *, phone_number: str, phone_code_hash: str, phone_code: str) -> None: ...

    class wallPapers(TLObject):
        hash: int
        wallpapers: list[TLObject]
        def __init__(self, *, hash: int, wallpapers: list[TLObject]) -> None: ...

    class wallPapersNotModified(TLObject):
        def __init__(self) -> None: ...

    class webAuthorizations(TLObject):
        authorizations: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, authorizations: list[TLObject], users: list[TLObject]) -> None: ...

    class webBrowserSettings(TLObject):
        open_external_browser: bool
        display_close_button: bool
        external_exceptions: list[TLObject]
        inapp_exceptions: list[TLObject]
        hash: int
        def __init__(self, *, open_external_browser: bool = ..., display_close_button: bool = ..., external_exceptions: list[TLObject], inapp_exceptions: list[TLObject], hash: int) -> None: ...

    class webBrowserSettingsNotModified(TLObject):
        def __init__(self) -> None: ...

class accountDaysTTL(TLObject):
    days: int
    def __init__(self, *, days: int) -> None: ...

class aiComposeTone(TLObject):
    creator: bool
    id: int
    access_hash: int
    slug: str
    title: str
    emoji_id: int | None
    prompt: str | None
    installs_count: int | None
    author_id: int | None
    example_english: TLObject | None
    def __init__(self, *, creator: bool = ..., id: int, access_hash: int, slug: str, title: str, emoji_id: int | None = ..., prompt: str | None = ..., installs_count: int | None = ..., author_id: int | None = ..., example_english: TLObject | None = ...) -> None: ...

class aiComposeToneDefault(TLObject):
    tone: str
    emoji_id: int
    title: str
    def __init__(self, *, tone: str, emoji_id: int, title: str) -> None: ...

class aiComposeToneExample(TLObject):
    from_: TLObject
    to: TLObject
    def __init__(self, *, from_: TLObject, to: TLObject) -> None: ...

class aicompose:
    class createTone(TLObject):
        display_author: bool
        emoji_id: int
        title: str
        prompt: str
        def __init__(self, *, display_author: bool = ..., emoji_id: int, title: str, prompt: str) -> None: ...

    class deleteTone(TLObject):
        tone: TLObject
        def __init__(self, *, tone: TLObject) -> None: ...

    class getTone(TLObject):
        tone: TLObject
        def __init__(self, *, tone: TLObject) -> None: ...

    class getToneExample(TLObject):
        tone: TLObject
        num: int
        def __init__(self, *, tone: TLObject, num: int) -> None: ...

    class getTones(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class saveTone(TLObject):
        tone: TLObject
        unsave: bool
        def __init__(self, *, tone: TLObject, unsave: bool) -> None: ...

    class tones(TLObject):
        hash: int
        tones: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, hash: int, tones: list[TLObject], users: list[TLObject]) -> None: ...

    class tonesNotModified(TLObject):
        def __init__(self) -> None: ...

    class updateTone(TLObject):
        tone: TLObject
        display_author: bool
        emoji_id: int | None
        title: str | None
        prompt: str | None
        def __init__(self, *, tone: TLObject, display_author: bool = ..., emoji_id: int | None = ..., title: str | None = ..., prompt: str | None = ...) -> None: ...

class attachMenuBot(TLObject):
    inactive: bool
    has_settings: bool
    request_write_access: bool
    show_in_attach_menu: bool
    show_in_side_menu: bool
    side_menu_disclaimer_needed: bool
    bot_id: int
    short_name: str
    peer_types: list[TLObject] | None
    icons: list[TLObject]
    def __init__(self, *, inactive: bool = ..., has_settings: bool = ..., request_write_access: bool = ..., show_in_attach_menu: bool = ..., show_in_side_menu: bool = ..., side_menu_disclaimer_needed: bool = ..., bot_id: int, short_name: str, peer_types: list[TLObject] | None = ..., icons: list[TLObject]) -> None: ...

class attachMenuBotIcon(TLObject):
    name: str
    icon: TLObject
    colors: list[TLObject] | None
    def __init__(self, *, name: str, icon: TLObject, colors: list[TLObject] | None = ...) -> None: ...

class attachMenuBotIconColor(TLObject):
    name: str
    color: int
    def __init__(self, *, name: str, color: int) -> None: ...

class attachMenuBots(TLObject):
    hash: int
    bots: list[TLObject]
    users: list[TLObject]
    def __init__(self, *, hash: int, bots: list[TLObject], users: list[TLObject]) -> None: ...

class attachMenuBotsBot(TLObject):
    bot: TLObject
    users: list[TLObject]
    def __init__(self, *, bot: TLObject, users: list[TLObject]) -> None: ...

class attachMenuBotsNotModified(TLObject):
    def __init__(self) -> None: ...

class attachMenuPeerTypeBotPM(TLObject):
    def __init__(self) -> None: ...

class attachMenuPeerTypeBroadcast(TLObject):
    def __init__(self) -> None: ...

class attachMenuPeerTypeChat(TLObject):
    def __init__(self) -> None: ...

class attachMenuPeerTypePM(TLObject):
    def __init__(self) -> None: ...

class attachMenuPeerTypeSameBotPM(TLObject):
    def __init__(self) -> None: ...

class auctionBidLevel(TLObject):
    pos: int
    amount: int
    date: int
    def __init__(self, *, pos: int, amount: int, date: int) -> None: ...

class auth:
    class acceptLoginToken(TLObject):
        token: bytes
        def __init__(self, *, token: bytes) -> None: ...

    class authorization(TLObject):
        setup_password_required: bool
        otherwise_relogin_days: int | None
        tmp_sessions: int | None
        future_auth_token: bytes | None
        user: TLObject
        def __init__(self, *, setup_password_required: bool = ..., otherwise_relogin_days: int | None = ..., tmp_sessions: int | None = ..., future_auth_token: bytes | None = ..., user: TLObject) -> None: ...

    class authorizationSignUpRequired(TLObject):
        terms_of_service: TLObject | None
        def __init__(self, *, terms_of_service: TLObject | None = ...) -> None: ...

    class bindTempAuthKey(TLObject):
        perm_auth_key_id: int
        nonce: int
        expires_at: int
        encrypted_message: bytes
        def __init__(self, *, perm_auth_key_id: int, nonce: int, expires_at: int, encrypted_message: bytes) -> None: ...

    class cancelCode(TLObject):
        phone_number: str
        phone_code_hash: str
        def __init__(self, *, phone_number: str, phone_code_hash: str) -> None: ...

    class cancelWebTokenAuthorization(TLObject):
        web_auth_token: str
        def __init__(self, *, web_auth_token: str) -> None: ...

    class checkPaidAuth(TLObject):
        phone_number: str
        phone_code_hash: str
        form_id: int
        def __init__(self, *, phone_number: str, phone_code_hash: str, form_id: int) -> None: ...

    class checkPassword(TLObject):
        password: TLObject
        def __init__(self, *, password: TLObject) -> None: ...

    class checkRecoveryPassword(TLObject):
        code: str
        def __init__(self, *, code: str) -> None: ...

    class codeTypeCall(TLObject):
        def __init__(self) -> None: ...

    class codeTypeFlashCall(TLObject):
        def __init__(self) -> None: ...

    class codeTypeFragmentSms(TLObject):
        def __init__(self) -> None: ...

    class codeTypeMissedCall(TLObject):
        def __init__(self) -> None: ...

    class codeTypeSms(TLObject):
        def __init__(self) -> None: ...

    class dropTempAuthKeys(TLObject):
        except_auth_keys: list[int]
        def __init__(self, *, except_auth_keys: list[int]) -> None: ...

    class exportAuthorization(TLObject):
        dc_id: int
        def __init__(self, *, dc_id: int) -> None: ...

    class exportLoginToken(TLObject):
        api_id: int
        api_hash: str
        except_ids: list[int]
        def __init__(self, *, api_id: int, api_hash: str, except_ids: list[int]) -> None: ...

    class exportedAuthorization(TLObject):
        id: int
        bytes: bytes
        def __init__(self, *, id: int, bytes: bytes) -> None: ...

    class finishFirebasePnvLogin(TLObject):
        google_token: str
        def __init__(self, *, google_token: str) -> None: ...

    class finishPasskeyLogin(TLObject):
        credential: TLObject
        from_dc_id: int | None
        from_auth_key_id: int | None
        def __init__(self, *, credential: TLObject, from_dc_id: int | None = ..., from_auth_key_id: int | None = ...) -> None: ...

    class firebasePnvIntent(TLObject):
        nonce: str
        digital_credential_payload: str
        def __init__(self, *, nonce: str, digital_credential_payload: str) -> None: ...

    class firebasePnvSignUp(TLObject):
        no_joined_notifications: bool
        first_name: str
        last_name: str
        def __init__(self, *, no_joined_notifications: bool = ..., first_name: str, last_name: str) -> None: ...

    class importAuthorization(TLObject):
        id: int
        bytes: bytes
        def __init__(self, *, id: int, bytes: bytes) -> None: ...

    class importBotAuthorization(TLObject):
        flags: int
        api_id: int
        api_hash: str
        bot_auth_token: str
        def __init__(self, *, flags: int, api_id: int, api_hash: str, bot_auth_token: str) -> None: ...

    class importLoginToken(TLObject):
        token: bytes
        def __init__(self, *, token: bytes) -> None: ...

    class importWebTokenAuthorization(TLObject):
        api_id: int
        api_hash: str
        web_auth_token: str
        def __init__(self, *, api_id: int, api_hash: str, web_auth_token: str) -> None: ...

    class initFirebasePnvLogin(TLObject):
        except_ids: list[int] | None
        api_id: int
        api_hash: str
        def __init__(self, *, except_ids: list[int] | None = ..., api_id: int, api_hash: str) -> None: ...

    class initPasskeyLogin(TLObject):
        api_id: int
        api_hash: str
        def __init__(self, *, api_id: int, api_hash: str) -> None: ...

    class logOut(TLObject):
        def __init__(self) -> None: ...

    class loggedOut(TLObject):
        future_auth_token: bytes | None
        def __init__(self, *, future_auth_token: bytes | None = ...) -> None: ...

    class loginToken(TLObject):
        expires: int
        token: bytes
        def __init__(self, *, expires: int, token: bytes) -> None: ...

    class loginTokenMigrateTo(TLObject):
        dc_id: int
        token: bytes
        def __init__(self, *, dc_id: int, token: bytes) -> None: ...

    class loginTokenSuccess(TLObject):
        authorization: TLObject
        def __init__(self, *, authorization: TLObject) -> None: ...

    class passkeyLoginOptions(TLObject):
        options: TLObject
        def __init__(self, *, options: TLObject) -> None: ...

    class passwordRecovery(TLObject):
        email_pattern: str
        def __init__(self, *, email_pattern: str) -> None: ...

    class recoverPassword(TLObject):
        code: str
        new_settings: TLObject | None
        def __init__(self, *, code: str, new_settings: TLObject | None = ...) -> None: ...

    class reportMissingCode(TLObject):
        phone_number: str
        phone_code_hash: str
        mnc: str
        def __init__(self, *, phone_number: str, phone_code_hash: str, mnc: str) -> None: ...

    class requestFirebaseSms(TLObject):
        phone_number: str
        phone_code_hash: str
        safety_net_token: str | None
        play_integrity_token: str | None
        ios_push_secret: str | None
        def __init__(self, *, phone_number: str, phone_code_hash: str, safety_net_token: str | None = ..., play_integrity_token: str | None = ..., ios_push_secret: str | None = ...) -> None: ...

    class requestPasswordRecovery(TLObject):
        def __init__(self) -> None: ...

    class resendCode(TLObject):
        phone_number: str
        phone_code_hash: str
        reason: str | None
        def __init__(self, *, phone_number: str, phone_code_hash: str, reason: str | None = ...) -> None: ...

    class resetAuthorizations(TLObject):
        def __init__(self) -> None: ...

    class resetLoginEmail(TLObject):
        phone_number: str
        phone_code_hash: str
        def __init__(self, *, phone_number: str, phone_code_hash: str) -> None: ...

    class sendCode(TLObject):
        phone_number: str
        api_id: int
        api_hash: str
        settings: TLObject
        def __init__(self, *, phone_number: str, api_id: int, api_hash: str, settings: TLObject) -> None: ...

    class sentCode(TLObject):
        type: TLObject
        phone_code_hash: str
        next_type: TLObject | None
        timeout: int | None
        def __init__(self, *, type: TLObject, phone_code_hash: str, next_type: TLObject | None = ..., timeout: int | None = ...) -> None: ...

    class sentCodePaymentRequired(TLObject):
        store_product: str
        phone_code_hash: str
        support_email_address: str
        support_email_subject: str
        premium_days: int
        currency: str
        amount: int
        def __init__(self, *, store_product: str, phone_code_hash: str, support_email_address: str, support_email_subject: str, premium_days: int, currency: str, amount: int) -> None: ...

    class sentCodeSuccess(TLObject):
        authorization: TLObject
        def __init__(self, *, authorization: TLObject) -> None: ...

    class sentCodeTypeApp(TLObject):
        length: int
        def __init__(self, *, length: int) -> None: ...

    class sentCodeTypeCall(TLObject):
        length: int
        def __init__(self, *, length: int) -> None: ...

    class sentCodeTypeEmailCode(TLObject):
        apple_signin_allowed: bool
        google_signin_allowed: bool
        email_pattern: str
        length: int
        reset_available_period: int | None
        reset_pending_date: int | None
        def __init__(self, *, apple_signin_allowed: bool = ..., google_signin_allowed: bool = ..., email_pattern: str, length: int, reset_available_period: int | None = ..., reset_pending_date: int | None = ...) -> None: ...

    class sentCodeTypeFirebaseSms(TLObject):
        nonce: bytes | None
        play_integrity_project_id: int | None
        play_integrity_nonce: bytes | None
        receipt: str | None
        push_timeout: int | None
        length: int
        def __init__(self, *, nonce: bytes | None = ..., play_integrity_project_id: int | None = ..., play_integrity_nonce: bytes | None = ..., receipt: str | None = ..., push_timeout: int | None = ..., length: int) -> None: ...

    class sentCodeTypeFlashCall(TLObject):
        pattern: str
        def __init__(self, *, pattern: str) -> None: ...

    class sentCodeTypeFragmentSms(TLObject):
        url: str
        length: int
        def __init__(self, *, url: str, length: int) -> None: ...

    class sentCodeTypeMissedCall(TLObject):
        prefix: str
        length: int
        def __init__(self, *, prefix: str, length: int) -> None: ...

    class sentCodeTypeSetUpEmailRequired(TLObject):
        apple_signin_allowed: bool
        google_signin_allowed: bool
        def __init__(self, *, apple_signin_allowed: bool = ..., google_signin_allowed: bool = ...) -> None: ...

    class sentCodeTypeSms(TLObject):
        length: int
        def __init__(self, *, length: int) -> None: ...

    class sentCodeTypeSmsPhrase(TLObject):
        beginning: str | None
        def __init__(self, *, beginning: str | None = ...) -> None: ...

    class sentCodeTypeSmsWord(TLObject):
        beginning: str | None
        def __init__(self, *, beginning: str | None = ...) -> None: ...

    class signIn(TLObject):
        phone_number: str
        phone_code_hash: str
        phone_code: str | None
        email_verification: TLObject | None
        def __init__(self, *, phone_number: str, phone_code_hash: str, phone_code: str | None = ..., email_verification: TLObject | None = ...) -> None: ...

    class signUp(TLObject):
        no_joined_notifications: bool
        phone_number: str
        phone_code_hash: str
        first_name: str
        last_name: str
        def __init__(self, *, no_joined_notifications: bool = ..., phone_number: str, phone_code_hash: str, first_name: str, last_name: str) -> None: ...

class authorization(TLObject):
    current: bool
    official_app: bool
    password_pending: bool
    encrypted_requests_disabled: bool
    call_requests_disabled: bool
    unconfirmed: bool
    hash: int
    device_model: str
    platform: str
    system_version: str
    api_id: int
    app_name: str
    app_version: str
    date_created: int
    date_active: int
    ip: str
    country: str
    region: str
    def __init__(self, *, current: bool = ..., official_app: bool = ..., password_pending: bool = ..., encrypted_requests_disabled: bool = ..., call_requests_disabled: bool = ..., unconfirmed: bool = ..., hash: int, device_model: str, platform: str, system_version: str, api_id: int, app_name: str, app_version: str, date_created: int, date_active: int, ip: str, country: str, region: str) -> None: ...

class autoDownloadSettings(TLObject):
    disabled: bool
    video_preload_large: bool
    audio_preload_next: bool
    phonecalls_less_data: bool
    stories_preload: bool
    photo_size_max: int
    video_size_max: int
    file_size_max: int
    video_upload_maxbitrate: int
    small_queue_active_operations_max: int
    large_queue_active_operations_max: int
    def __init__(self, *, disabled: bool = ..., video_preload_large: bool = ..., audio_preload_next: bool = ..., phonecalls_less_data: bool = ..., stories_preload: bool = ..., photo_size_max: int, video_size_max: int, file_size_max: int, video_upload_maxbitrate: int, small_queue_active_operations_max: int, large_queue_active_operations_max: int) -> None: ...

class autoSaveException(TLObject):
    peer: TLObject
    settings: TLObject
    def __init__(self, *, peer: TLObject, settings: TLObject) -> None: ...

class autoSaveSettings(TLObject):
    photos: bool
    videos: bool
    video_max_size: int | None
    def __init__(self, *, photos: bool = ..., videos: bool = ..., video_max_size: int | None = ...) -> None: ...

class availableEffect(TLObject):
    premium_required: bool
    id: int
    emoticon: str
    static_icon_id: int | None
    effect_sticker_id: int
    effect_animation_id: int | None
    def __init__(self, *, premium_required: bool = ..., id: int, emoticon: str, static_icon_id: int | None = ..., effect_sticker_id: int, effect_animation_id: int | None = ...) -> None: ...

class availableReaction(TLObject):
    inactive: bool
    premium: bool
    reaction: str
    title: str
    static_icon: TLObject
    appear_animation: TLObject
    select_animation: TLObject
    activate_animation: TLObject
    effect_animation: TLObject
    around_animation: TLObject | None
    center_icon: TLObject | None
    def __init__(self, *, inactive: bool = ..., premium: bool = ..., reaction: str, title: str, static_icon: TLObject, appear_animation: TLObject, select_animation: TLObject, activate_animation: TLObject, effect_animation: TLObject, around_animation: TLObject | None = ..., center_icon: TLObject | None = ...) -> None: ...

class bankCardOpenUrl(TLObject):
    url: str
    name: str
    def __init__(self, *, url: str, name: str) -> None: ...

class baseThemeArctic(TLObject):
    def __init__(self) -> None: ...

class baseThemeClassic(TLObject):
    def __init__(self) -> None: ...

class baseThemeDay(TLObject):
    def __init__(self) -> None: ...

class baseThemeNight(TLObject):
    def __init__(self) -> None: ...

class baseThemeTinted(TLObject):
    def __init__(self) -> None: ...

class birthday(TLObject):
    day: int
    month: int
    year: int | None
    def __init__(self, *, day: int, month: int, year: int | None = ...) -> None: ...

class boolFalse(TLObject):
    def __init__(self) -> None: ...

class boolTrue(TLObject):
    def __init__(self) -> None: ...

class boost(TLObject):
    gift: bool
    giveaway: bool
    unclaimed: bool
    id: str
    user_id: int | None
    giveaway_msg_id: int | None
    date: int
    expires: int
    used_gift_slug: str | None
    multiplier: int | None
    stars: int | None
    def __init__(self, *, gift: bool = ..., giveaway: bool = ..., unclaimed: bool = ..., id: str, user_id: int | None = ..., giveaway_msg_id: int | None = ..., date: int, expires: int, used_gift_slug: str | None = ..., multiplier: int | None = ..., stars: int | None = ...) -> None: ...

class botApp(TLObject):
    id: int
    access_hash: int
    short_name: str
    title: str
    description: str
    photo: TLObject
    document: TLObject | None
    hash: int
    def __init__(self, *, id: int, access_hash: int, short_name: str, title: str, description: str, photo: TLObject, document: TLObject | None = ..., hash: int) -> None: ...

class botAppNotModified(TLObject):
    def __init__(self) -> None: ...

class botAppSettings(TLObject):
    placeholder_path: bytes | None
    background_color: int | None
    background_dark_color: int | None
    header_color: int | None
    header_dark_color: int | None
    def __init__(self, *, placeholder_path: bytes | None = ..., background_color: int | None = ..., background_dark_color: int | None = ..., header_color: int | None = ..., header_dark_color: int | None = ...) -> None: ...

class botBusinessConnection(TLObject):
    disabled: bool
    connection_id: str
    user_id: int
    dc_id: int
    date: int
    rights: TLObject | None
    def __init__(self, *, disabled: bool = ..., connection_id: str, user_id: int, dc_id: int, date: int, rights: TLObject | None = ...) -> None: ...

class botCommand(TLObject):
    ephemeral: bool
    command: str
    description: str
    def __init__(self, *, ephemeral: bool = ..., command: str, description: str) -> None: ...

class botCommandScopeChatAdmins(TLObject):
    def __init__(self) -> None: ...

class botCommandScopeChats(TLObject):
    def __init__(self) -> None: ...

class botCommandScopeDefault(TLObject):
    def __init__(self) -> None: ...

class botCommandScopePeer(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class botCommandScopePeerAdmins(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class botCommandScopePeerUser(TLObject):
    peer: TLObject
    user_id: TLObject
    def __init__(self, *, peer: TLObject, user_id: TLObject) -> None: ...

class botCommandScopeUsers(TLObject):
    def __init__(self) -> None: ...

class botInfo(TLObject):
    has_preview_medias: bool
    user_id: int | None
    description: str | None
    description_photo: TLObject | None
    description_document: TLObject | None
    commands: list[TLObject] | None
    menu_button: TLObject | None
    privacy_policy_url: str | None
    app_settings: TLObject | None
    verifier_settings: TLObject | None
    def __init__(self, *, has_preview_medias: bool = ..., user_id: int | None = ..., description: str | None = ..., description_photo: TLObject | None = ..., description_document: TLObject | None = ..., commands: list[TLObject] | None = ..., menu_button: TLObject | None = ..., privacy_policy_url: str | None = ..., app_settings: TLObject | None = ..., verifier_settings: TLObject | None = ...) -> None: ...

class botInlineMediaResult(TLObject):
    id: str
    type: str
    photo: TLObject | None
    document: TLObject | None
    title: str | None
    description: str | None
    send_message: TLObject
    def __init__(self, *, id: str, type: str, photo: TLObject | None = ..., document: TLObject | None = ..., title: str | None = ..., description: str | None = ..., send_message: TLObject) -> None: ...

class botInlineMessageMediaAuto(TLObject):
    invert_media: bool
    message: str
    entities: list[TLObject] | None
    reply_markup: TLObject | None
    def __init__(self, *, invert_media: bool = ..., message: str, entities: list[TLObject] | None = ..., reply_markup: TLObject | None = ...) -> None: ...

class botInlineMessageMediaContact(TLObject):
    phone_number: str
    first_name: str
    last_name: str
    vcard: str
    reply_markup: TLObject | None
    def __init__(self, *, phone_number: str, first_name: str, last_name: str, vcard: str, reply_markup: TLObject | None = ...) -> None: ...

class botInlineMessageMediaGeo(TLObject):
    geo: TLObject
    heading: int | None
    period: int | None
    proximity_notification_radius: int | None
    reply_markup: TLObject | None
    def __init__(self, *, geo: TLObject, heading: int | None = ..., period: int | None = ..., proximity_notification_radius: int | None = ..., reply_markup: TLObject | None = ...) -> None: ...

class botInlineMessageMediaInvoice(TLObject):
    shipping_address_requested: bool
    test: bool
    title: str
    description: str
    photo: TLObject | None
    currency: str
    total_amount: int
    reply_markup: TLObject | None
    def __init__(self, *, shipping_address_requested: bool = ..., test: bool = ..., title: str, description: str, photo: TLObject | None = ..., currency: str, total_amount: int, reply_markup: TLObject | None = ...) -> None: ...

class botInlineMessageMediaVenue(TLObject):
    geo: TLObject
    title: str
    address: str
    provider: str
    venue_id: str
    venue_type: str
    reply_markup: TLObject | None
    def __init__(self, *, geo: TLObject, title: str, address: str, provider: str, venue_id: str, venue_type: str, reply_markup: TLObject | None = ...) -> None: ...

class botInlineMessageMediaWebPage(TLObject):
    invert_media: bool
    force_large_media: bool
    force_small_media: bool
    manual: bool
    safe: bool
    message: str
    entities: list[TLObject] | None
    url: str
    reply_markup: TLObject | None
    def __init__(self, *, invert_media: bool = ..., force_large_media: bool = ..., force_small_media: bool = ..., manual: bool = ..., safe: bool = ..., message: str, entities: list[TLObject] | None = ..., url: str, reply_markup: TLObject | None = ...) -> None: ...

class botInlineMessageRichMessage(TLObject):
    reply_markup: TLObject | None
    rich_message: TLObject
    def __init__(self, *, reply_markup: TLObject | None = ..., rich_message: TLObject) -> None: ...

class botInlineMessageText(TLObject):
    no_webpage: bool
    invert_media: bool
    message: str
    entities: list[TLObject] | None
    reply_markup: TLObject | None
    def __init__(self, *, no_webpage: bool = ..., invert_media: bool = ..., message: str, entities: list[TLObject] | None = ..., reply_markup: TLObject | None = ...) -> None: ...

class botInlineMessageWidget(TLObject):
    invert_media: bool
    width: int
    height: int
    payload: bytes
    public_data: str | None
    public_data_hash: int | None
    chat_data: str | None
    reply_markup: TLObject | None
    widget_id: int | None
    message: str
    entities: list[TLObject] | None
    def __init__(self, *, invert_media: bool = ..., width: int, height: int, payload: bytes, public_data: str | None = ..., public_data_hash: int | None = ..., chat_data: str | None = ..., reply_markup: TLObject | None = ..., widget_id: int | None = ..., message: str, entities: list[TLObject] | None = ...) -> None: ...

class botInlineResult(TLObject):
    id: str
    type: str
    title: str | None
    description: str | None
    url: str | None
    thumb: TLObject | None
    content: TLObject | None
    send_message: TLObject
    def __init__(self, *, id: str, type: str, title: str | None = ..., description: str | None = ..., url: str | None = ..., thumb: TLObject | None = ..., content: TLObject | None = ..., send_message: TLObject) -> None: ...

class botMenuButton(TLObject):
    text: str
    url: str
    def __init__(self, *, text: str, url: str) -> None: ...

class botMenuButtonCommands(TLObject):
    def __init__(self) -> None: ...

class botMenuButtonDefault(TLObject):
    def __init__(self) -> None: ...

class botPreviewMedia(TLObject):
    date: int
    media: TLObject
    def __init__(self, *, date: int, media: TLObject) -> None: ...

class botVerification(TLObject):
    bot_id: int
    icon: int
    description: TLObject
    def __init__(self, *, bot_id: int, icon: int, description: TLObject) -> None: ...

class botVerifierSettings(TLObject):
    can_modify_custom_description: bool
    icon: int
    company: str
    custom_description: TLObject | None
    def __init__(self, *, can_modify_custom_description: bool = ..., icon: int, company: str, custom_description: TLObject | None = ...) -> None: ...

class bots:
    class accessSettings(TLObject):
        restricted: bool
        add_users: list[TLObject] | None
        def __init__(self, *, restricted: bool = ..., add_users: list[TLObject] | None = ...) -> None: ...

    class addPreviewMedia(TLObject):
        bot: TLObject
        lang_code: str
        media: TLObject
        def __init__(self, *, bot: TLObject, lang_code: str, media: TLObject) -> None: ...

    class addUsername(TLObject):
        bot: TLObject
        username: str
        def __init__(self, *, bot: TLObject, username: str) -> None: ...

    class allowSendMessage(TLObject):
        bot: TLObject
        def __init__(self, *, bot: TLObject) -> None: ...

    class answerWebhookJSONQuery(TLObject):
        query_id: int
        data: TLObject
        def __init__(self, *, query_id: int, data: TLObject) -> None: ...

    class botInfo(TLObject):
        name: str
        about: str
        description: str
        def __init__(self, *, name: str, about: str, description: str) -> None: ...

    class canSendMessage(TLObject):
        bot: TLObject
        def __init__(self, *, bot: TLObject) -> None: ...

    class checkDownloadFileParams(TLObject):
        bot: TLObject
        file_name: str
        url: str
        def __init__(self, *, bot: TLObject, file_name: str, url: str) -> None: ...

    class checkUsername(TLObject):
        additional: bool
        username: str
        def __init__(self, *, additional: bool = ..., username: str) -> None: ...

    class createBot(TLObject):
        via_deeplink: bool
        name: str
        username: str
        manager_id: TLObject
        def __init__(self, *, via_deeplink: bool = ..., name: str, username: str, manager_id: TLObject) -> None: ...

    class deletePreviewMedia(TLObject):
        bot: TLObject
        lang_code: str
        media: list[TLObject]
        def __init__(self, *, bot: TLObject, lang_code: str, media: list[TLObject]) -> None: ...

    class editAccessSettings(TLObject):
        restricted: bool
        bot: TLObject
        add_users: list[TLObject] | None
        def __init__(self, *, restricted: bool = ..., bot: TLObject, add_users: list[TLObject] | None = ...) -> None: ...

    class editPreviewMedia(TLObject):
        bot: TLObject
        lang_code: str
        media: TLObject
        new_media: TLObject
        def __init__(self, *, bot: TLObject, lang_code: str, media: TLObject, new_media: TLObject) -> None: ...

    class exportBotToken(TLObject):
        bot: TLObject
        revoke: bool
        def __init__(self, *, bot: TLObject, revoke: bool) -> None: ...

    class exportedBotToken(TLObject):
        token: str
        def __init__(self, *, token: str) -> None: ...

    class getAccessSettings(TLObject):
        bot: TLObject
        def __init__(self, *, bot: TLObject) -> None: ...

    class getAdminedBots(TLObject):
        def __init__(self) -> None: ...

    class getBotCommands(TLObject):
        scope: TLObject
        lang_code: str
        def __init__(self, *, scope: TLObject, lang_code: str) -> None: ...

    class getBotInfo(TLObject):
        bot: TLObject | None
        lang_code: str
        def __init__(self, *, bot: TLObject | None = ..., lang_code: str) -> None: ...

    class getBotMenuButton(TLObject):
        user_id: TLObject
        def __init__(self, *, user_id: TLObject) -> None: ...

    class getBotRecommendations(TLObject):
        bot: TLObject
        def __init__(self, *, bot: TLObject) -> None: ...

    class getPopularAppBots(TLObject):
        offset: str
        limit: int
        def __init__(self, *, offset: str, limit: int) -> None: ...

    class getPreviewInfo(TLObject):
        bot: TLObject
        lang_code: str
        def __init__(self, *, bot: TLObject, lang_code: str) -> None: ...

    class getPreviewMedias(TLObject):
        bot: TLObject
        def __init__(self, *, bot: TLObject) -> None: ...

    class getRequestedWebViewButton(TLObject):
        bot: TLObject
        webapp_req_id: str
        def __init__(self, *, bot: TLObject, webapp_req_id: str) -> None: ...

    class invokeWebViewCustomMethod(TLObject):
        bot: TLObject
        custom_method: str
        params: TLObject
        def __init__(self, *, bot: TLObject, custom_method: str, params: TLObject) -> None: ...

    class popularAppBots(TLObject):
        next_offset: str | None
        users: list[TLObject]
        def __init__(self, *, next_offset: str | None = ..., users: list[TLObject]) -> None: ...

    class previewInfo(TLObject):
        media: list[TLObject]
        lang_codes: list[str]
        def __init__(self, *, media: list[TLObject], lang_codes: list[str]) -> None: ...

    class removeUsername(TLObject):
        bot: TLObject
        username: str
        def __init__(self, *, bot: TLObject, username: str) -> None: ...

    class reorderPreviewMedias(TLObject):
        bot: TLObject
        lang_code: str
        order: list[TLObject]
        def __init__(self, *, bot: TLObject, lang_code: str, order: list[TLObject]) -> None: ...

    class reorderUsernames(TLObject):
        bot: TLObject
        order: list[str]
        def __init__(self, *, bot: TLObject, order: list[str]) -> None: ...

    class requestWebViewButton(TLObject):
        user_id: TLObject
        button: TLObject
        def __init__(self, *, user_id: TLObject, button: TLObject) -> None: ...

    class requestedButton(TLObject):
        webapp_req_id: str
        def __init__(self, *, webapp_req_id: str) -> None: ...

    class resetBotCommands(TLObject):
        scope: TLObject
        lang_code: str
        def __init__(self, *, scope: TLObject, lang_code: str) -> None: ...

    class sendCustomRequest(TLObject):
        custom_method: str
        params: TLObject
        def __init__(self, *, custom_method: str, params: TLObject) -> None: ...

    class setBotBroadcastDefaultAdminRights(TLObject):
        admin_rights: TLObject
        def __init__(self, *, admin_rights: TLObject) -> None: ...

    class setBotCommands(TLObject):
        scope: TLObject
        lang_code: str
        commands: list[TLObject]
        def __init__(self, *, scope: TLObject, lang_code: str, commands: list[TLObject]) -> None: ...

    class setBotGroupDefaultAdminRights(TLObject):
        admin_rights: TLObject
        def __init__(self, *, admin_rights: TLObject) -> None: ...

    class setBotInfo(TLObject):
        bot: TLObject | None
        lang_code: str
        name: str | None
        about: str | None
        description: str | None
        def __init__(self, *, bot: TLObject | None = ..., lang_code: str, name: str | None = ..., about: str | None = ..., description: str | None = ...) -> None: ...

    class setBotMenuButton(TLObject):
        user_id: TLObject
        button: TLObject
        def __init__(self, *, user_id: TLObject, button: TLObject) -> None: ...

    class setCustomVerification(TLObject):
        enabled: bool
        bot: TLObject | None
        peer: TLObject
        custom_description: TLObject | None
        def __init__(self, *, enabled: bool = ..., bot: TLObject | None = ..., peer: TLObject, custom_description: TLObject | None = ...) -> None: ...

    class setJoinChatResults(TLObject):
        query_id: int
        result: TLObject
        def __init__(self, *, query_id: int, result: TLObject) -> None: ...

    class toggleUserEmojiStatusPermission(TLObject):
        bot: TLObject
        enabled: bool
        def __init__(self, *, bot: TLObject, enabled: bool) -> None: ...

    class toggleUsername(TLObject):
        bot: TLObject
        username: str
        active: bool
        def __init__(self, *, bot: TLObject, username: str, active: bool) -> None: ...

    class updateStarRefProgram(TLObject):
        bot: TLObject
        commission_permille: int
        duration_months: int | None
        def __init__(self, *, bot: TLObject, commission_permille: int, duration_months: int | None = ...) -> None: ...

    class updateUserEmojiStatus(TLObject):
        user_id: TLObject
        emoji_status: TLObject
        def __init__(self, *, user_id: TLObject, emoji_status: TLObject) -> None: ...

class businessAwayMessage(TLObject):
    offline_only: bool
    shortcut_id: int
    schedule: TLObject
    recipients: TLObject
    def __init__(self, *, offline_only: bool = ..., shortcut_id: int, schedule: TLObject, recipients: TLObject) -> None: ...

class businessAwayMessageScheduleAlways(TLObject):
    def __init__(self) -> None: ...

class businessAwayMessageScheduleCustom(TLObject):
    start_date: int
    end_date: int
    def __init__(self, *, start_date: int, end_date: int) -> None: ...

class businessAwayMessageScheduleOutsideWorkHours(TLObject):
    def __init__(self) -> None: ...

class businessBotRecipients(TLObject):
    existing_chats: bool
    new_chats: bool
    contacts: bool
    non_contacts: bool
    exclude_selected: bool
    users: list[int] | None
    exclude_users: list[int] | None
    def __init__(self, *, existing_chats: bool = ..., new_chats: bool = ..., contacts: bool = ..., non_contacts: bool = ..., exclude_selected: bool = ..., users: list[int] | None = ..., exclude_users: list[int] | None = ...) -> None: ...

class businessBotRights(TLObject):
    reply: bool
    read_messages: bool
    delete_sent_messages: bool
    delete_received_messages: bool
    edit_name: bool
    edit_bio: bool
    edit_profile_photo: bool
    edit_username: bool
    view_gifts: bool
    sell_gifts: bool
    change_gift_settings: bool
    transfer_and_upgrade_gifts: bool
    transfer_stars: bool
    manage_stories: bool
    def __init__(self, *, reply: bool = ..., read_messages: bool = ..., delete_sent_messages: bool = ..., delete_received_messages: bool = ..., edit_name: bool = ..., edit_bio: bool = ..., edit_profile_photo: bool = ..., edit_username: bool = ..., view_gifts: bool = ..., sell_gifts: bool = ..., change_gift_settings: bool = ..., transfer_and_upgrade_gifts: bool = ..., transfer_stars: bool = ..., manage_stories: bool = ...) -> None: ...

class businessChatLink(TLObject):
    link: str
    message: str
    entities: list[TLObject] | None
    title: str | None
    views: int
    def __init__(self, *, link: str, message: str, entities: list[TLObject] | None = ..., title: str | None = ..., views: int) -> None: ...

class businessGreetingMessage(TLObject):
    shortcut_id: int
    recipients: TLObject
    no_activity_days: int
    def __init__(self, *, shortcut_id: int, recipients: TLObject, no_activity_days: int) -> None: ...

class businessIntro(TLObject):
    title: str
    description: str
    sticker: TLObject | None
    def __init__(self, *, title: str, description: str, sticker: TLObject | None = ...) -> None: ...

class businessLocation(TLObject):
    geo_point: TLObject | None
    address: str
    def __init__(self, *, geo_point: TLObject | None = ..., address: str) -> None: ...

class businessRecipients(TLObject):
    existing_chats: bool
    new_chats: bool
    contacts: bool
    non_contacts: bool
    exclude_selected: bool
    users: list[int] | None
    def __init__(self, *, existing_chats: bool = ..., new_chats: bool = ..., contacts: bool = ..., non_contacts: bool = ..., exclude_selected: bool = ..., users: list[int] | None = ...) -> None: ...

class businessWeeklyOpen(TLObject):
    start_minute: int
    end_minute: int
    def __init__(self, *, start_minute: int, end_minute: int) -> None: ...

class businessWorkHours(TLObject):
    open_now: bool
    timezone_id: str
    weekly_open: list[TLObject]
    def __init__(self, *, open_now: bool = ..., timezone_id: str, weekly_open: list[TLObject]) -> None: ...

class buttonTypeDefault(TLObject):
    def __init__(self) -> None: ...

class buttonTypeRequestGeoLocation(TLObject):
    def __init__(self) -> None: ...

class buttonTypeRequestPeer(TLObject):
    button_id: int
    peer_type: TLObject
    max_quantity: int
    def __init__(self, *, button_id: int, peer_type: TLObject, max_quantity: int) -> None: ...

class buttonTypeRequestPhone(TLObject):
    def __init__(self) -> None: ...

class buttonTypeRequestPoll(TLObject):
    quiz: bool
    def __init__(self, *, quiz: bool = ...) -> None: ...

class buttonTypeSimpleWebView(TLObject):
    url: str
    def __init__(self, *, url: str) -> None: ...

class cdnConfig(TLObject):
    public_keys: list[TLObject]
    def __init__(self, *, public_keys: list[TLObject]) -> None: ...

class cdnPublicKey(TLObject):
    dc_id: int
    public_key: str
    def __init__(self, *, dc_id: int, public_key: str) -> None: ...

class channel(TLObject):
    creator: bool
    left: bool
    broadcast: bool
    verified: bool
    megagroup: bool
    restricted: bool
    signatures: bool
    min: bool
    scam: bool
    has_link: bool
    has_geo: bool
    slowmode_enabled: bool
    call_active: bool
    call_not_empty: bool
    fake: bool
    gigagroup: bool
    noforwards: bool
    join_to_send: bool
    join_request: bool
    forum: bool
    stories_hidden: bool
    stories_hidden_min: bool
    stories_unavailable: bool
    signature_profiles: bool
    autotranslation: bool
    broadcast_messages_allowed: bool
    monoforum: bool
    forum_tabs: bool
    in_news: bool
    forum_sidebar: bool
    id: int
    access_hash: int | None
    title: str
    username: str | None
    photo: TLObject
    date: int
    restriction_reason: list[TLObject] | None
    admin_rights: TLObject | None
    banned_rights: TLObject | None
    default_banned_rights: TLObject | None
    participants_count: int | None
    usernames: list[TLObject] | None
    stories_max_id: TLObject | None
    color: TLObject | None
    profile_color: TLObject | None
    emoji_status: TLObject | None
    level: int | None
    subscription_until_date: int | None
    bot_verification_icon: int | None
    send_paid_messages_stars: int | None
    linked_monoforum_id: int | None
    linked_community_id: int | None
    pinned_msg_id: int | None
    def __init__(self, *, creator: bool = ..., left: bool = ..., broadcast: bool = ..., verified: bool = ..., megagroup: bool = ..., restricted: bool = ..., signatures: bool = ..., min: bool = ..., scam: bool = ..., has_link: bool = ..., has_geo: bool = ..., slowmode_enabled: bool = ..., call_active: bool = ..., call_not_empty: bool = ..., fake: bool = ..., gigagroup: bool = ..., noforwards: bool = ..., join_to_send: bool = ..., join_request: bool = ..., forum: bool = ..., stories_hidden: bool = ..., stories_hidden_min: bool = ..., stories_unavailable: bool = ..., signature_profiles: bool = ..., autotranslation: bool = ..., broadcast_messages_allowed: bool = ..., monoforum: bool = ..., forum_tabs: bool = ..., in_news: bool = ..., forum_sidebar: bool = ..., id: int, access_hash: int | None = ..., title: str, username: str | None = ..., photo: TLObject, date: int, restriction_reason: list[TLObject] | None = ..., admin_rights: TLObject | None = ..., banned_rights: TLObject | None = ..., default_banned_rights: TLObject | None = ..., participants_count: int | None = ..., usernames: list[TLObject] | None = ..., stories_max_id: TLObject | None = ..., color: TLObject | None = ..., profile_color: TLObject | None = ..., emoji_status: TLObject | None = ..., level: int | None = ..., subscription_until_date: int | None = ..., bot_verification_icon: int | None = ..., send_paid_messages_stars: int | None = ..., linked_monoforum_id: int | None = ..., linked_community_id: int | None = ..., pinned_msg_id: int | None = ...) -> None: ...

class channelAdminLogEvent(TLObject):
    id: int
    date: int
    user_id: int
    action: TLObject
    def __init__(self, *, id: int, date: int, user_id: int, action: TLObject) -> None: ...

class channelAdminLogEventActionChangeAbout(TLObject):
    prev_value: str
    new_value: str
    def __init__(self, *, prev_value: str, new_value: str) -> None: ...

class channelAdminLogEventActionChangeAvailableReactions(TLObject):
    prev_value: TLObject
    new_value: TLObject
    def __init__(self, *, prev_value: TLObject, new_value: TLObject) -> None: ...

class channelAdminLogEventActionChangeEmojiStatus(TLObject):
    prev_value: TLObject
    new_value: TLObject
    def __init__(self, *, prev_value: TLObject, new_value: TLObject) -> None: ...

class channelAdminLogEventActionChangeEmojiStickerSet(TLObject):
    prev_stickerset: TLObject
    new_stickerset: TLObject
    def __init__(self, *, prev_stickerset: TLObject, new_stickerset: TLObject) -> None: ...

class channelAdminLogEventActionChangeHistoryTTL(TLObject):
    prev_value: int
    new_value: int
    def __init__(self, *, prev_value: int, new_value: int) -> None: ...

class channelAdminLogEventActionChangeLinkedChat(TLObject):
    prev_value: int
    new_value: int
    def __init__(self, *, prev_value: int, new_value: int) -> None: ...

class channelAdminLogEventActionChangeLocation(TLObject):
    prev_value: TLObject
    new_value: TLObject
    def __init__(self, *, prev_value: TLObject, new_value: TLObject) -> None: ...

class channelAdminLogEventActionChangePeerColor(TLObject):
    prev_value: TLObject
    new_value: TLObject
    def __init__(self, *, prev_value: TLObject, new_value: TLObject) -> None: ...

class channelAdminLogEventActionChangePhoto(TLObject):
    prev_photo: TLObject
    new_photo: TLObject
    def __init__(self, *, prev_photo: TLObject, new_photo: TLObject) -> None: ...

class channelAdminLogEventActionChangeProfilePeerColor(TLObject):
    prev_value: TLObject
    new_value: TLObject
    def __init__(self, *, prev_value: TLObject, new_value: TLObject) -> None: ...

class channelAdminLogEventActionChangeStickerSet(TLObject):
    prev_stickerset: TLObject
    new_stickerset: TLObject
    def __init__(self, *, prev_stickerset: TLObject, new_stickerset: TLObject) -> None: ...

class channelAdminLogEventActionChangeTitle(TLObject):
    prev_value: str
    new_value: str
    def __init__(self, *, prev_value: str, new_value: str) -> None: ...

class channelAdminLogEventActionChangeUsername(TLObject):
    prev_value: str
    new_value: str
    def __init__(self, *, prev_value: str, new_value: str) -> None: ...

class channelAdminLogEventActionChangeUsernames(TLObject):
    prev_value: list[str]
    new_value: list[str]
    def __init__(self, *, prev_value: list[str], new_value: list[str]) -> None: ...

class channelAdminLogEventActionChangeWallpaper(TLObject):
    prev_value: TLObject
    new_value: TLObject
    def __init__(self, *, prev_value: TLObject, new_value: TLObject) -> None: ...

class channelAdminLogEventActionCreateTopic(TLObject):
    topic: TLObject
    def __init__(self, *, topic: TLObject) -> None: ...

class channelAdminLogEventActionDefaultBannedRights(TLObject):
    prev_banned_rights: TLObject
    new_banned_rights: TLObject
    def __init__(self, *, prev_banned_rights: TLObject, new_banned_rights: TLObject) -> None: ...

class channelAdminLogEventActionDeleteMessage(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class channelAdminLogEventActionDeleteTopic(TLObject):
    topic: TLObject
    def __init__(self, *, topic: TLObject) -> None: ...

class channelAdminLogEventActionDiscardGroupCall(TLObject):
    call: TLObject
    def __init__(self, *, call: TLObject) -> None: ...

class channelAdminLogEventActionEditMessage(TLObject):
    prev_message: TLObject
    new_message: TLObject
    def __init__(self, *, prev_message: TLObject, new_message: TLObject) -> None: ...

class channelAdminLogEventActionEditTopic(TLObject):
    prev_topic: TLObject
    new_topic: TLObject
    def __init__(self, *, prev_topic: TLObject, new_topic: TLObject) -> None: ...

class channelAdminLogEventActionExportedInviteDelete(TLObject):
    invite: TLObject
    def __init__(self, *, invite: TLObject) -> None: ...

class channelAdminLogEventActionExportedInviteEdit(TLObject):
    prev_invite: TLObject
    new_invite: TLObject
    def __init__(self, *, prev_invite: TLObject, new_invite: TLObject) -> None: ...

class channelAdminLogEventActionExportedInviteRevoke(TLObject):
    invite: TLObject
    def __init__(self, *, invite: TLObject) -> None: ...

class channelAdminLogEventActionParticipantEditRank(TLObject):
    user_id: int
    prev_rank: str
    new_rank: str
    def __init__(self, *, user_id: int, prev_rank: str, new_rank: str) -> None: ...

class channelAdminLogEventActionParticipantInvite(TLObject):
    participant: TLObject
    def __init__(self, *, participant: TLObject) -> None: ...

class channelAdminLogEventActionParticipantJoin(TLObject):
    def __init__(self) -> None: ...

class channelAdminLogEventActionParticipantJoinByInvite(TLObject):
    via_chatlist: bool
    invite: TLObject
    def __init__(self, *, via_chatlist: bool = ..., invite: TLObject) -> None: ...

class channelAdminLogEventActionParticipantJoinByRequest(TLObject):
    invite: TLObject
    approved_by: int
    def __init__(self, *, invite: TLObject, approved_by: int) -> None: ...

class channelAdminLogEventActionParticipantLeave(TLObject):
    def __init__(self) -> None: ...

class channelAdminLogEventActionParticipantMute(TLObject):
    participant: TLObject
    def __init__(self, *, participant: TLObject) -> None: ...

class channelAdminLogEventActionParticipantSubExtend(TLObject):
    prev_participant: TLObject
    new_participant: TLObject
    def __init__(self, *, prev_participant: TLObject, new_participant: TLObject) -> None: ...

class channelAdminLogEventActionParticipantToggleAdmin(TLObject):
    prev_participant: TLObject
    new_participant: TLObject
    def __init__(self, *, prev_participant: TLObject, new_participant: TLObject) -> None: ...

class channelAdminLogEventActionParticipantToggleBan(TLObject):
    prev_participant: TLObject
    new_participant: TLObject
    def __init__(self, *, prev_participant: TLObject, new_participant: TLObject) -> None: ...

class channelAdminLogEventActionParticipantUnmute(TLObject):
    participant: TLObject
    def __init__(self, *, participant: TLObject) -> None: ...

class channelAdminLogEventActionParticipantVolume(TLObject):
    participant: TLObject
    def __init__(self, *, participant: TLObject) -> None: ...

class channelAdminLogEventActionPinTopic(TLObject):
    prev_topic: TLObject | None
    new_topic: TLObject | None
    def __init__(self, *, prev_topic: TLObject | None = ..., new_topic: TLObject | None = ...) -> None: ...

class channelAdminLogEventActionSendMessage(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class channelAdminLogEventActionStartGroupCall(TLObject):
    call: TLObject
    def __init__(self, *, call: TLObject) -> None: ...

class channelAdminLogEventActionStopPoll(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class channelAdminLogEventActionToggleAntiSpam(TLObject):
    new_value: bool
    def __init__(self, *, new_value: bool) -> None: ...

class channelAdminLogEventActionToggleAutotranslation(TLObject):
    new_value: bool
    def __init__(self, *, new_value: bool) -> None: ...

class channelAdminLogEventActionToggleForum(TLObject):
    new_value: bool
    def __init__(self, *, new_value: bool) -> None: ...

class channelAdminLogEventActionToggleGroupCallSetting(TLObject):
    join_muted: bool
    def __init__(self, *, join_muted: bool) -> None: ...

class channelAdminLogEventActionToggleInvites(TLObject):
    new_value: bool
    def __init__(self, *, new_value: bool) -> None: ...

class channelAdminLogEventActionToggleNoForwards(TLObject):
    new_value: bool
    def __init__(self, *, new_value: bool) -> None: ...

class channelAdminLogEventActionTogglePreHistoryHidden(TLObject):
    new_value: bool
    def __init__(self, *, new_value: bool) -> None: ...

class channelAdminLogEventActionToggleSignatureProfiles(TLObject):
    new_value: bool
    def __init__(self, *, new_value: bool) -> None: ...

class channelAdminLogEventActionToggleSignatures(TLObject):
    new_value: bool
    def __init__(self, *, new_value: bool) -> None: ...

class channelAdminLogEventActionToggleSlowMode(TLObject):
    prev_value: int
    new_value: int
    def __init__(self, *, prev_value: int, new_value: int) -> None: ...

class channelAdminLogEventActionUpdatePinned(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class channelAdminLogEventsFilter(TLObject):
    join: bool
    leave: bool
    invite: bool
    ban: bool
    unban: bool
    kick: bool
    unkick: bool
    promote: bool
    demote: bool
    info: bool
    settings: bool
    pinned: bool
    edit: bool
    delete: bool
    group_call: bool
    invites: bool
    send: bool
    forums: bool
    sub_extend: bool
    edit_rank: bool
    def __init__(self, *, join: bool = ..., leave: bool = ..., invite: bool = ..., ban: bool = ..., unban: bool = ..., kick: bool = ..., unkick: bool = ..., promote: bool = ..., demote: bool = ..., info: bool = ..., settings: bool = ..., pinned: bool = ..., edit: bool = ..., delete: bool = ..., group_call: bool = ..., invites: bool = ..., send: bool = ..., forums: bool = ..., sub_extend: bool = ..., edit_rank: bool = ...) -> None: ...

class channelForbidden(TLObject):
    broadcast: bool
    megagroup: bool
    monoforum: bool
    id: int
    access_hash: int
    title: str
    until_date: int | None
    def __init__(self, *, broadcast: bool = ..., megagroup: bool = ..., monoforum: bool = ..., id: int, access_hash: int, title: str, until_date: int | None = ...) -> None: ...

class channelFull(TLObject):
    can_view_participants: bool
    can_set_username: bool
    can_set_stickers: bool
    hidden_prehistory: bool
    can_set_location: bool
    has_scheduled: bool
    can_view_stats: bool
    blocked: bool
    can_delete_channel: bool
    antispam: bool
    participants_hidden: bool
    translations_disabled: bool
    stories_pinned_available: bool
    view_forum_as_messages: bool
    restricted_sponsored: bool
    can_view_revenue: bool
    paid_media_allowed: bool
    can_view_stars_revenue: bool
    paid_reactions_available: bool
    stargifts_available: bool
    paid_messages_available: bool
    has_welcome_messages: bool
    id: int
    about: str
    participants_count: int | None
    admins_count: int | None
    kicked_count: int | None
    banned_count: int | None
    online_count: int | None
    read_inbox_max_id: int
    read_outbox_max_id: int
    unread_count: int
    chat_photo: TLObject
    notify_settings: TLObject
    exported_invite: TLObject | None
    bot_info: list[TLObject]
    migrated_from_chat_id: int | None
    migrated_from_max_id: int | None
    pinned_msg_id: int | None
    stickerset: TLObject | None
    available_min_id: int | None
    folder_id: int | None
    linked_chat_id: int | None
    location: TLObject | None
    slowmode_seconds: int | None
    slowmode_next_send_date: int | None
    stats_dc: int | None
    pts: int
    call: TLObject | None
    ttl_period: int | None
    pending_suggestions: list[str] | None
    groupcall_default_join_as: TLObject | None
    theme_emoticon: str | None
    requests_pending: int | None
    recent_requesters: list[int] | None
    default_send_as: TLObject | None
    available_reactions: TLObject | None
    reactions_limit: int | None
    stories: TLObject | None
    wallpaper: TLObject | None
    boosts_applied: int | None
    boosts_unrestrict: int | None
    emojiset: TLObject | None
    bot_verification: TLObject | None
    stargifts_count: int | None
    send_paid_messages_stars: int | None
    main_tab: TLObject | None
    guard_bot_id: int | None
    share_theme: TLObject | None
    def __init__(self, *, can_view_participants: bool = ..., can_set_username: bool = ..., can_set_stickers: bool = ..., hidden_prehistory: bool = ..., can_set_location: bool = ..., has_scheduled: bool = ..., can_view_stats: bool = ..., blocked: bool = ..., can_delete_channel: bool = ..., antispam: bool = ..., participants_hidden: bool = ..., translations_disabled: bool = ..., stories_pinned_available: bool = ..., view_forum_as_messages: bool = ..., restricted_sponsored: bool = ..., can_view_revenue: bool = ..., paid_media_allowed: bool = ..., can_view_stars_revenue: bool = ..., paid_reactions_available: bool = ..., stargifts_available: bool = ..., paid_messages_available: bool = ..., has_welcome_messages: bool = ..., id: int, about: str, participants_count: int | None = ..., admins_count: int | None = ..., kicked_count: int | None = ..., banned_count: int | None = ..., online_count: int | None = ..., read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, chat_photo: TLObject, notify_settings: TLObject, exported_invite: TLObject | None = ..., bot_info: list[TLObject], migrated_from_chat_id: int | None = ..., migrated_from_max_id: int | None = ..., pinned_msg_id: int | None = ..., stickerset: TLObject | None = ..., available_min_id: int | None = ..., folder_id: int | None = ..., linked_chat_id: int | None = ..., location: TLObject | None = ..., slowmode_seconds: int | None = ..., slowmode_next_send_date: int | None = ..., stats_dc: int | None = ..., pts: int, call: TLObject | None = ..., ttl_period: int | None = ..., pending_suggestions: list[str] | None = ..., groupcall_default_join_as: TLObject | None = ..., theme_emoticon: str | None = ..., requests_pending: int | None = ..., recent_requesters: list[int] | None = ..., default_send_as: TLObject | None = ..., available_reactions: TLObject | None = ..., reactions_limit: int | None = ..., stories: TLObject | None = ..., wallpaper: TLObject | None = ..., boosts_applied: int | None = ..., boosts_unrestrict: int | None = ..., emojiset: TLObject | None = ..., bot_verification: TLObject | None = ..., stargifts_count: int | None = ..., send_paid_messages_stars: int | None = ..., main_tab: TLObject | None = ..., guard_bot_id: int | None = ..., share_theme: TLObject | None = ...) -> None: ...

class channelLocation(TLObject):
    geo_point: TLObject
    address: str
    def __init__(self, *, geo_point: TLObject, address: str) -> None: ...

class channelLocationEmpty(TLObject):
    def __init__(self) -> None: ...

class channelMessagesFilter(TLObject):
    exclude_new_messages: bool
    ranges: list[TLObject]
    def __init__(self, *, exclude_new_messages: bool = ..., ranges: list[TLObject]) -> None: ...

class channelMessagesFilterEmpty(TLObject):
    def __init__(self) -> None: ...

class channelParticipant(TLObject):
    user_id: int
    date: int
    subscription_until_date: int | None
    rank: str | None
    def __init__(self, *, user_id: int, date: int, subscription_until_date: int | None = ..., rank: str | None = ...) -> None: ...

class channelParticipantAdmin(TLObject):
    can_edit: bool
    self_: bool
    user_id: int
    inviter_id: int | None
    promoted_by: int
    date: int
    admin_rights: TLObject
    rank: str | None
    def __init__(self, *, can_edit: bool = ..., self_: bool = ..., user_id: int, inviter_id: int | None = ..., promoted_by: int, date: int, admin_rights: TLObject, rank: str | None = ...) -> None: ...

class channelParticipantBanned(TLObject):
    left: bool
    peer: TLObject
    kicked_by: int
    date: int
    banned_rights: TLObject
    rank: str | None
    def __init__(self, *, left: bool = ..., peer: TLObject, kicked_by: int, date: int, banned_rights: TLObject, rank: str | None = ...) -> None: ...

class channelParticipantCreator(TLObject):
    user_id: int
    admin_rights: TLObject
    rank: str | None
    def __init__(self, *, user_id: int, admin_rights: TLObject, rank: str | None = ...) -> None: ...

class channelParticipantLeft(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class channelParticipantSelf(TLObject):
    via_request: bool
    user_id: int
    inviter_id: int
    date: int
    subscription_until_date: int | None
    rank: str | None
    def __init__(self, *, via_request: bool = ..., user_id: int, inviter_id: int, date: int, subscription_until_date: int | None = ..., rank: str | None = ...) -> None: ...

class channelParticipantsAdmins(TLObject):
    def __init__(self) -> None: ...

class channelParticipantsBanned(TLObject):
    q: str
    def __init__(self, *, q: str) -> None: ...

class channelParticipantsBots(TLObject):
    def __init__(self) -> None: ...

class channelParticipantsContacts(TLObject):
    q: str
    def __init__(self, *, q: str) -> None: ...

class channelParticipantsKicked(TLObject):
    q: str
    def __init__(self, *, q: str) -> None: ...

class channelParticipantsMentions(TLObject):
    q: str | None
    top_msg_id: int | None
    def __init__(self, *, q: str | None = ..., top_msg_id: int | None = ...) -> None: ...

class channelParticipantsRecent(TLObject):
    def __init__(self) -> None: ...

class channelParticipantsSearch(TLObject):
    q: str
    def __init__(self, *, q: str) -> None: ...

class channels:
    class adminLogResults(TLObject):
        events: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, events: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class channelParticipant(TLObject):
        participant: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, participant: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class channelParticipants(TLObject):
        count: int
        participants: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, participants: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class channelParticipantsNotModified(TLObject):
        def __init__(self) -> None: ...

    class checkSearchPostsFlood(TLObject):
        query: str | None
        def __init__(self, *, query: str | None = ...) -> None: ...

    class checkUsername(TLObject):
        channel: TLObject
        username: str
        def __init__(self, *, channel: TLObject, username: str) -> None: ...

    class convertToGigagroup(TLObject):
        channel: TLObject
        def __init__(self, *, channel: TLObject) -> None: ...

    class createChannel(TLObject):
        broadcast: bool
        megagroup: bool
        for_import: bool
        forum: bool
        title: str
        about: str
        geo_point: TLObject | None
        address: str | None
        ttl_period: int | None
        def __init__(self, *, broadcast: bool = ..., megagroup: bool = ..., for_import: bool = ..., forum: bool = ..., title: str, about: str, geo_point: TLObject | None = ..., address: str | None = ..., ttl_period: int | None = ...) -> None: ...

    class deactivateAllUsernames(TLObject):
        channel: TLObject
        def __init__(self, *, channel: TLObject) -> None: ...

    class deleteChannel(TLObject):
        channel: TLObject
        def __init__(self, *, channel: TLObject) -> None: ...

    class deleteHistory(TLObject):
        for_everyone: bool
        channel: TLObject
        max_id: int
        def __init__(self, *, for_everyone: bool = ..., channel: TLObject, max_id: int) -> None: ...

    class deleteMessages(TLObject):
        channel: TLObject
        id: list[int]
        def __init__(self, *, channel: TLObject, id: list[int]) -> None: ...

    class deleteParticipantHistory(TLObject):
        channel: TLObject
        participant: TLObject
        def __init__(self, *, channel: TLObject, participant: TLObject) -> None: ...

    class editAdmin(TLObject):
        channel: TLObject
        user_id: TLObject
        admin_rights: TLObject
        rank: str | None
        def __init__(self, *, channel: TLObject, user_id: TLObject, admin_rights: TLObject, rank: str | None = ...) -> None: ...

    class editBanned(TLObject):
        channel: TLObject
        participant: TLObject
        banned_rights: TLObject
        def __init__(self, *, channel: TLObject, participant: TLObject, banned_rights: TLObject) -> None: ...

    class editLocation(TLObject):
        channel: TLObject
        geo_point: TLObject
        address: str
        def __init__(self, *, channel: TLObject, geo_point: TLObject, address: str) -> None: ...

    class editPhoto(TLObject):
        channel: TLObject
        photo: TLObject
        def __init__(self, *, channel: TLObject, photo: TLObject) -> None: ...

    class editTitle(TLObject):
        channel: TLObject
        title: str
        def __init__(self, *, channel: TLObject, title: str) -> None: ...

    class exportMessageLink(TLObject):
        grouped: bool
        thread: bool
        channel: TLObject
        id: int
        def __init__(self, *, grouped: bool = ..., thread: bool = ..., channel: TLObject, id: int) -> None: ...

    class getAdminLog(TLObject):
        channel: TLObject
        q: str
        events_filter: TLObject | None
        admins: list[TLObject] | None
        max_id: int
        min_id: int
        limit: int
        def __init__(self, *, channel: TLObject, q: str, events_filter: TLObject | None = ..., admins: list[TLObject] | None = ..., max_id: int, min_id: int, limit: int) -> None: ...

    class getAdminedPublicChannels(TLObject):
        by_location: bool
        check_limit: bool
        for_personal: bool
        for_community_peer: bool
        def __init__(self, *, by_location: bool = ..., check_limit: bool = ..., for_personal: bool = ..., for_community_peer: bool = ...) -> None: ...

    class getChannelRecommendations(TLObject):
        channel: TLObject | None
        def __init__(self, *, channel: TLObject | None = ...) -> None: ...

    class getChannels(TLObject):
        id: list[TLObject]
        def __init__(self, *, id: list[TLObject]) -> None: ...

    class getFullChannel(TLObject):
        channel: TLObject
        def __init__(self, *, channel: TLObject) -> None: ...

    class getGroupsForDiscussion(TLObject):
        def __init__(self) -> None: ...

    class getInactiveChannels(TLObject):
        def __init__(self) -> None: ...

    class getLeftChannels(TLObject):
        offset: int
        def __init__(self, *, offset: int) -> None: ...

    class getMessageAuthor(TLObject):
        channel: TLObject
        id: int
        def __init__(self, *, channel: TLObject, id: int) -> None: ...

    class getMessages(TLObject):
        channel: TLObject
        id: list[TLObject]
        def __init__(self, *, channel: TLObject, id: list[TLObject]) -> None: ...

    class getParticipant(TLObject):
        channel: TLObject
        participant: TLObject
        def __init__(self, *, channel: TLObject, participant: TLObject) -> None: ...

    class getParticipants(TLObject):
        channel: TLObject
        filter: TLObject
        offset: int
        limit: int
        hash: int
        def __init__(self, *, channel: TLObject, filter: TLObject, offset: int, limit: int, hash: int) -> None: ...

    class getSendAs(TLObject):
        for_paid_reactions: bool
        for_live_stories: bool
        peer: TLObject
        def __init__(self, *, for_paid_reactions: bool = ..., for_live_stories: bool = ..., peer: TLObject) -> None: ...

    class inviteToChannel(TLObject):
        channel: TLObject
        users: list[TLObject]
        def __init__(self, *, channel: TLObject, users: list[TLObject]) -> None: ...

    class joinChannel(TLObject):
        channel: TLObject
        def __init__(self, *, channel: TLObject) -> None: ...

    class leaveChannel(TLObject):
        channel: TLObject
        def __init__(self, *, channel: TLObject) -> None: ...

    class readHistory(TLObject):
        channel: TLObject
        max_id: int
        def __init__(self, *, channel: TLObject, max_id: int) -> None: ...

    class readMessageContents(TLObject):
        channel: TLObject
        id: list[int]
        def __init__(self, *, channel: TLObject, id: list[int]) -> None: ...

    class reorderUsernames(TLObject):
        channel: TLObject
        order: list[str]
        def __init__(self, *, channel: TLObject, order: list[str]) -> None: ...

    class reportAntiSpamFalsePositive(TLObject):
        channel: TLObject
        msg_id: int
        def __init__(self, *, channel: TLObject, msg_id: int) -> None: ...

    class reportSpam(TLObject):
        channel: TLObject
        participant: TLObject
        id: list[int]
        def __init__(self, *, channel: TLObject, participant: TLObject, id: list[int]) -> None: ...

    class restrictSponsoredMessages(TLObject):
        channel: TLObject
        restricted: bool
        def __init__(self, *, channel: TLObject, restricted: bool) -> None: ...

    class searchPosts(TLObject):
        hashtag: str | None
        query: str | None
        offset_rate: int
        offset_peer: TLObject
        offset_id: int
        limit: int
        allow_paid_stars: int | None
        def __init__(self, *, hashtag: str | None = ..., query: str | None = ..., offset_rate: int, offset_peer: TLObject, offset_id: int, limit: int, allow_paid_stars: int | None = ...) -> None: ...

    class sendAsPeers(TLObject):
        peers: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, peers: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class setBoostsToUnblockRestrictions(TLObject):
        channel: TLObject
        boosts: int
        def __init__(self, *, channel: TLObject, boosts: int) -> None: ...

    class setDiscussionGroup(TLObject):
        broadcast: TLObject
        group: TLObject
        def __init__(self, *, broadcast: TLObject, group: TLObject) -> None: ...

    class setEmojiStickers(TLObject):
        channel: TLObject
        stickerset: TLObject
        def __init__(self, *, channel: TLObject, stickerset: TLObject) -> None: ...

    class setMainProfileTab(TLObject):
        channel: TLObject
        tab: TLObject
        def __init__(self, *, channel: TLObject, tab: TLObject) -> None: ...

    class setStickers(TLObject):
        channel: TLObject
        stickerset: TLObject
        def __init__(self, *, channel: TLObject, stickerset: TLObject) -> None: ...

    class sponsoredMessageReportResultAdsHidden(TLObject):
        def __init__(self) -> None: ...

    class sponsoredMessageReportResultChooseOption(TLObject):
        title: str
        options: list[TLObject]
        def __init__(self, *, title: str, options: list[TLObject]) -> None: ...

    class sponsoredMessageReportResultReported(TLObject):
        def __init__(self) -> None: ...

    class toggleAntiSpam(TLObject):
        channel: TLObject
        enabled: bool
        def __init__(self, *, channel: TLObject, enabled: bool) -> None: ...

    class toggleAutotranslation(TLObject):
        channel: TLObject
        enabled: bool
        def __init__(self, *, channel: TLObject, enabled: bool) -> None: ...

    class toggleForum(TLObject):
        channel: TLObject
        enabled: bool
        tabs: bool
        sidebar: bool
        def __init__(self, *, channel: TLObject, enabled: bool, tabs: bool, sidebar: bool) -> None: ...

    class toggleJoinRequest(TLObject):
        apply_to_invites: bool
        channel: TLObject
        enabled: bool
        guard_bot: TLObject | None
        def __init__(self, *, apply_to_invites: bool = ..., channel: TLObject, enabled: bool, guard_bot: TLObject | None = ...) -> None: ...

    class toggleJoinToSend(TLObject):
        channel: TLObject
        enabled: bool
        def __init__(self, *, channel: TLObject, enabled: bool) -> None: ...

    class toggleParticipantsHidden(TLObject):
        channel: TLObject
        enabled: bool
        def __init__(self, *, channel: TLObject, enabled: bool) -> None: ...

    class togglePreHistoryHidden(TLObject):
        channel: TLObject
        enabled: bool
        def __init__(self, *, channel: TLObject, enabled: bool) -> None: ...

    class toggleSignatures(TLObject):
        signatures_enabled: bool
        profiles_enabled: bool
        channel: TLObject
        def __init__(self, *, signatures_enabled: bool = ..., profiles_enabled: bool = ..., channel: TLObject) -> None: ...

    class toggleSlowMode(TLObject):
        channel: TLObject
        seconds: int
        def __init__(self, *, channel: TLObject, seconds: int) -> None: ...

    class toggleUsername(TLObject):
        channel: TLObject
        username: str
        active: bool
        def __init__(self, *, channel: TLObject, username: str, active: bool) -> None: ...

    class toggleViewForumAsMessages(TLObject):
        channel: TLObject
        enabled: bool
        def __init__(self, *, channel: TLObject, enabled: bool) -> None: ...

    class updateColor(TLObject):
        for_profile: bool
        channel: TLObject
        color: int | None
        background_emoji_id: int | None
        def __init__(self, *, for_profile: bool = ..., channel: TLObject, color: int | None = ..., background_emoji_id: int | None = ...) -> None: ...

    class updateEmojiStatus(TLObject):
        channel: TLObject
        emoji_status: TLObject
        def __init__(self, *, channel: TLObject, emoji_status: TLObject) -> None: ...

    class updatePaidMessagesPrice(TLObject):
        broadcast_messages_allowed: bool
        channel: TLObject
        send_paid_messages_stars: int
        def __init__(self, *, broadcast_messages_allowed: bool = ..., channel: TLObject, send_paid_messages_stars: int) -> None: ...

    class updateUsername(TLObject):
        channel: TLObject
        username: str
        def __init__(self, *, channel: TLObject, username: str) -> None: ...

class chat(TLObject):
    creator: bool
    left: bool
    deactivated: bool
    call_active: bool
    call_not_empty: bool
    noforwards: bool
    id: int
    title: str
    photo: TLObject
    participants_count: int
    date: int
    version: int
    migrated_to: TLObject | None
    admin_rights: TLObject | None
    default_banned_rights: TLObject | None
    def __init__(self, *, creator: bool = ..., left: bool = ..., deactivated: bool = ..., call_active: bool = ..., call_not_empty: bool = ..., noforwards: bool = ..., id: int, title: str, photo: TLObject, participants_count: int, date: int, version: int, migrated_to: TLObject | None = ..., admin_rights: TLObject | None = ..., default_banned_rights: TLObject | None = ...) -> None: ...

class chatAdminRights(TLObject):
    change_info: bool
    post_messages: bool
    edit_messages: bool
    delete_messages: bool
    ban_users: bool
    invite_users: bool
    pin_messages: bool
    add_admins: bool
    anonymous: bool
    manage_call: bool
    other: bool
    manage_topics: bool
    post_stories: bool
    edit_stories: bool
    delete_stories: bool
    manage_direct_messages: bool
    manage_ranks: bool
    manage_linked_peers: bool
    manage_welcome_messages: bool
    def __init__(self, *, change_info: bool = ..., post_messages: bool = ..., edit_messages: bool = ..., delete_messages: bool = ..., ban_users: bool = ..., invite_users: bool = ..., pin_messages: bool = ..., add_admins: bool = ..., anonymous: bool = ..., manage_call: bool = ..., other: bool = ..., manage_topics: bool = ..., post_stories: bool = ..., edit_stories: bool = ..., delete_stories: bool = ..., manage_direct_messages: bool = ..., manage_ranks: bool = ..., manage_linked_peers: bool = ..., manage_welcome_messages: bool = ...) -> None: ...

class chatAdminWithInvites(TLObject):
    admin_id: int
    invites_count: int
    revoked_invites_count: int
    def __init__(self, *, admin_id: int, invites_count: int, revoked_invites_count: int) -> None: ...

class chatBannedRights(TLObject):
    view_messages: bool
    send_messages: bool
    send_media: bool
    send_stickers: bool
    send_gifs: bool
    send_games: bool
    send_inline: bool
    embed_links: bool
    send_polls: bool
    change_info: bool
    invite_users: bool
    pin_messages: bool
    manage_topics: bool
    send_photos: bool
    send_videos: bool
    send_roundvideos: bool
    send_audios: bool
    send_voices: bool
    send_docs: bool
    send_plain: bool
    edit_rank: bool
    send_reactions: bool
    manage_linked_peers: bool
    until_date: int
    def __init__(self, *, view_messages: bool = ..., send_messages: bool = ..., send_media: bool = ..., send_stickers: bool = ..., send_gifs: bool = ..., send_games: bool = ..., send_inline: bool = ..., embed_links: bool = ..., send_polls: bool = ..., change_info: bool = ..., invite_users: bool = ..., pin_messages: bool = ..., manage_topics: bool = ..., send_photos: bool = ..., send_videos: bool = ..., send_roundvideos: bool = ..., send_audios: bool = ..., send_voices: bool = ..., send_docs: bool = ..., send_plain: bool = ..., edit_rank: bool = ..., send_reactions: bool = ..., manage_linked_peers: bool = ..., until_date: int) -> None: ...

class chatEmpty(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class chatForbidden(TLObject):
    id: int
    title: str
    def __init__(self, *, id: int, title: str) -> None: ...

class chatFull(TLObject):
    can_set_username: bool
    has_scheduled: bool
    translations_disabled: bool
    has_welcome_messages: bool
    id: int
    about: str
    participants: TLObject
    chat_photo: TLObject | None
    notify_settings: TLObject
    exported_invite: TLObject | None
    bot_info: list[TLObject] | None
    pinned_msg_id: int | None
    folder_id: int | None
    call: TLObject | None
    ttl_period: int | None
    groupcall_default_join_as: TLObject | None
    theme_emoticon: str | None
    requests_pending: int | None
    recent_requesters: list[int] | None
    available_reactions: TLObject | None
    reactions_limit: int | None
    def __init__(self, *, can_set_username: bool = ..., has_scheduled: bool = ..., translations_disabled: bool = ..., has_welcome_messages: bool = ..., id: int, about: str, participants: TLObject, chat_photo: TLObject | None = ..., notify_settings: TLObject, exported_invite: TLObject | None = ..., bot_info: list[TLObject] | None = ..., pinned_msg_id: int | None = ..., folder_id: int | None = ..., call: TLObject | None = ..., ttl_period: int | None = ..., groupcall_default_join_as: TLObject | None = ..., theme_emoticon: str | None = ..., requests_pending: int | None = ..., recent_requesters: list[int] | None = ..., available_reactions: TLObject | None = ..., reactions_limit: int | None = ...) -> None: ...

class chatInvite(TLObject):
    channel: bool
    broadcast: bool
    public: bool
    megagroup: bool
    request_needed: bool
    verified: bool
    scam: bool
    fake: bool
    can_refulfill_subscription: bool
    title: str
    about: str | None
    photo: TLObject
    participants_count: int
    participants: list[TLObject] | None
    color: int
    subscription_pricing: TLObject | None
    subscription_form_id: int | None
    bot_verification: TLObject | None
    def __init__(self, *, channel: bool = ..., broadcast: bool = ..., public: bool = ..., megagroup: bool = ..., request_needed: bool = ..., verified: bool = ..., scam: bool = ..., fake: bool = ..., can_refulfill_subscription: bool = ..., title: str, about: str | None = ..., photo: TLObject, participants_count: int, participants: list[TLObject] | None = ..., color: int, subscription_pricing: TLObject | None = ..., subscription_form_id: int | None = ..., bot_verification: TLObject | None = ...) -> None: ...

class chatInviteAlready(TLObject):
    chat: TLObject
    def __init__(self, *, chat: TLObject) -> None: ...

class chatInviteExported(TLObject):
    revoked: bool
    permanent: bool
    request_needed: bool
    link: str
    admin_id: int
    date: int
    start_date: int | None
    expire_date: int | None
    usage_limit: int | None
    usage: int | None
    requested: int | None
    subscription_expired: int | None
    title: str | None
    subscription_pricing: TLObject | None
    def __init__(self, *, revoked: bool = ..., permanent: bool = ..., request_needed: bool = ..., link: str, admin_id: int, date: int, start_date: int | None = ..., expire_date: int | None = ..., usage_limit: int | None = ..., usage: int | None = ..., requested: int | None = ..., subscription_expired: int | None = ..., title: str | None = ..., subscription_pricing: TLObject | None = ...) -> None: ...

class chatInviteImporter(TLObject):
    requested: bool
    via_chatlist: bool
    user_id: int
    date: int
    about: str | None
    approved_by: int | None
    def __init__(self, *, requested: bool = ..., via_chatlist: bool = ..., user_id: int, date: int, about: str | None = ..., approved_by: int | None = ...) -> None: ...

class chatInvitePeek(TLObject):
    chat: TLObject
    expires: int
    def __init__(self, *, chat: TLObject, expires: int) -> None: ...

class chatInvitePublicJoinRequests(TLObject):
    def __init__(self) -> None: ...

class chatOnlines(TLObject):
    onlines: int
    def __init__(self, *, onlines: int) -> None: ...

class chatParticipant(TLObject):
    user_id: int
    inviter_id: int
    date: int
    rank: str | None
    def __init__(self, *, user_id: int, inviter_id: int, date: int, rank: str | None = ...) -> None: ...

class chatParticipantAdmin(TLObject):
    user_id: int
    inviter_id: int
    date: int
    rank: str | None
    def __init__(self, *, user_id: int, inviter_id: int, date: int, rank: str | None = ...) -> None: ...

class chatParticipantCreator(TLObject):
    user_id: int
    rank: str | None
    def __init__(self, *, user_id: int, rank: str | None = ...) -> None: ...

class chatParticipants(TLObject):
    chat_id: int
    participants: list[TLObject]
    version: int
    def __init__(self, *, chat_id: int, participants: list[TLObject], version: int) -> None: ...

class chatParticipantsForbidden(TLObject):
    chat_id: int
    self_participant: TLObject | None
    def __init__(self, *, chat_id: int, self_participant: TLObject | None = ...) -> None: ...

class chatPhoto(TLObject):
    has_video: bool
    photo_id: int
    stripped_thumb: bytes | None
    dc_id: int
    def __init__(self, *, has_video: bool = ..., photo_id: int, stripped_thumb: bytes | None = ..., dc_id: int) -> None: ...

class chatPhotoEmpty(TLObject):
    def __init__(self) -> None: ...

class chatReactionsAll(TLObject):
    allow_custom: bool
    def __init__(self, *, allow_custom: bool = ...) -> None: ...

class chatReactionsNone(TLObject):
    def __init__(self) -> None: ...

class chatReactionsSome(TLObject):
    reactions: list[TLObject]
    def __init__(self, *, reactions: list[TLObject]) -> None: ...

class chatTheme(TLObject):
    emoticon: str
    def __init__(self, *, emoticon: str) -> None: ...

class chatThemeUniqueGift(TLObject):
    gift: TLObject
    theme_settings: list[TLObject]
    def __init__(self, *, gift: TLObject, theme_settings: list[TLObject]) -> None: ...

class chatlists:
    class chatlistInvite(TLObject):
        title_noanimate: bool
        title: TLObject
        emoticon: str | None
        peers: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, title_noanimate: bool = ..., title: TLObject, emoticon: str | None = ..., peers: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class chatlistInviteAlready(TLObject):
        filter_id: int
        missing_peers: list[TLObject]
        already_peers: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, filter_id: int, missing_peers: list[TLObject], already_peers: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class chatlistUpdates(TLObject):
        missing_peers: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, missing_peers: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class checkChatlistInvite(TLObject):
        slug: str
        def __init__(self, *, slug: str) -> None: ...

    class deleteExportedInvite(TLObject):
        chatlist: TLObject
        slug: str
        def __init__(self, *, chatlist: TLObject, slug: str) -> None: ...

    class editExportedInvite(TLObject):
        chatlist: TLObject
        slug: str
        title: str | None
        peers: list[TLObject] | None
        def __init__(self, *, chatlist: TLObject, slug: str, title: str | None = ..., peers: list[TLObject] | None = ...) -> None: ...

    class exportChatlistInvite(TLObject):
        chatlist: TLObject
        title: str
        peers: list[TLObject]
        def __init__(self, *, chatlist: TLObject, title: str, peers: list[TLObject]) -> None: ...

    class exportedChatlistInvite(TLObject):
        filter: TLObject
        invite: TLObject
        def __init__(self, *, filter: TLObject, invite: TLObject) -> None: ...

    class exportedInvites(TLObject):
        invites: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, invites: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class getChatlistUpdates(TLObject):
        chatlist: TLObject
        def __init__(self, *, chatlist: TLObject) -> None: ...

    class getExportedInvites(TLObject):
        chatlist: TLObject
        def __init__(self, *, chatlist: TLObject) -> None: ...

    class getLeaveChatlistSuggestions(TLObject):
        chatlist: TLObject
        def __init__(self, *, chatlist: TLObject) -> None: ...

    class hideChatlistUpdates(TLObject):
        chatlist: TLObject
        def __init__(self, *, chatlist: TLObject) -> None: ...

    class joinChatlistInvite(TLObject):
        slug: str
        peers: list[TLObject]
        def __init__(self, *, slug: str, peers: list[TLObject]) -> None: ...

    class joinChatlistUpdates(TLObject):
        chatlist: TLObject
        peers: list[TLObject]
        def __init__(self, *, chatlist: TLObject, peers: list[TLObject]) -> None: ...

    class leaveChatlist(TLObject):
        chatlist: TLObject
        peers: list[TLObject]
        def __init__(self, *, chatlist: TLObject, peers: list[TLObject]) -> None: ...

class codeSettings(TLObject):
    allow_flashcall: bool
    current_number: bool
    allow_app_hash: bool
    allow_missed_call: bool
    allow_firebase: bool
    unknown_number: bool
    logout_tokens: list[bytes] | None
    token: str | None
    app_sandbox: bool
    def __init__(self, *, allow_flashcall: bool = ..., current_number: bool = ..., allow_app_hash: bool = ..., allow_missed_call: bool = ..., allow_firebase: bool = ..., unknown_number: bool = ..., logout_tokens: list[bytes] | None = ..., token: str | None = ..., app_sandbox: bool = ...) -> None: ...

class communities:
    class create(TLObject):
        hidden: bool
        title: str
        about: str | None
        peer: TLObject
        def __init__(self, *, hidden: bool = ..., title: str, about: str | None = ..., peer: TLObject) -> None: ...

    class getJoinedCommunities(TLObject):
        def __init__(self) -> None: ...

    class getParticipantJoinedChats(TLObject):
        community: TLObject
        participant: TLObject
        def __init__(self, *, community: TLObject, participant: TLObject) -> None: ...

    class getPeerLinkRequests(TLObject):
        community: TLObject
        offset: str
        limit: int
        def __init__(self, *, community: TLObject, offset: str, limit: int) -> None: ...

    class participantJoinedChats(TLObject):
        creator_chat_ids: list[int]
        joined_chat_ids: list[int]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, creator_chat_ids: list[int], joined_chat_ids: list[int], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class peerLinkRequests(TLObject):
        total_count: int
        requests: list[TLObject]
        next_offset: str | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, total_count: int, requests: list[TLObject], next_offset: str | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class toggleAllPeerLinkRequestApproval(TLObject):
        reject: bool
        community: TLObject
        def __init__(self, *, reject: bool = ..., community: TLObject) -> None: ...

    class toggleCommunityCollapsedInDialogs(TLObject):
        collapsed: bool
        community: TLObject
        def __init__(self, *, collapsed: bool = ..., community: TLObject) -> None: ...

    class toggleParticipantBanned(TLObject):
        unban: bool
        community: TLObject
        participant: TLObject
        def __init__(self, *, unban: bool = ..., community: TLObject, participant: TLObject) -> None: ...

    class togglePeerLink(TLObject):
        visible: bool
        hidden: bool
        deleted: bool
        community: TLObject
        peer: TLObject
        def __init__(self, *, visible: bool = ..., hidden: bool = ..., deleted: bool = ..., community: TLObject, peer: TLObject) -> None: ...

    class togglePeerLinkRequestApproval(TLObject):
        reject: bool
        community: TLObject
        peer: TLObject
        def __init__(self, *, reject: bool = ..., community: TLObject, peer: TLObject) -> None: ...

class community(TLObject):
    creator: bool
    left: bool
    min: bool
    collapsed_in_dialogs: bool
    id: int
    access_hash: int | None
    title: str
    photo: TLObject
    date: int
    admin_rights: TLObject | None
    default_banned_rights: TLObject | None
    def __init__(self, *, creator: bool = ..., left: bool = ..., min: bool = ..., collapsed_in_dialogs: bool = ..., id: int, access_hash: int | None = ..., title: str, photo: TLObject, date: int, admin_rights: TLObject | None = ..., default_banned_rights: TLObject | None = ...) -> None: ...

class communityForbidden(TLObject):
    id: int
    access_hash: int | None
    title: str
    def __init__(self, *, id: int, access_hash: int | None = ..., title: str) -> None: ...

class communityFull(TLObject):
    id: int
    about: str
    chat_photo: TLObject
    linked_peers: list[TLObject]
    admins_count: int | None
    kicked_count: int | None
    peer_link_requests_pending: int | None
    def __init__(self, *, id: int, about: str, chat_photo: TLObject, linked_peers: list[TLObject], admins_count: int | None = ..., kicked_count: int | None = ..., peer_link_requests_pending: int | None = ...) -> None: ...

class communityPeer(TLObject):
    can_view_history: bool
    visible: bool
    peer: TLObject
    def __init__(self, *, can_view_history: bool = ..., visible: bool = ..., peer: TLObject) -> None: ...

class communityPeerRequest(TLObject):
    visible: bool
    peer: TLObject
    requested_by: int
    date: int
    def __init__(self, *, visible: bool = ..., peer: TLObject, requested_by: int, date: int) -> None: ...

class config(TLObject):
    default_p2p_contacts: bool
    preload_featured_stickers: bool
    revoke_pm_inbox: bool
    blocked_mode: bool
    force_try_ipv6: bool
    date: int
    expires: int
    test_mode: bool
    this_dc: int
    dc_options: list[TLObject]
    dc_txt_domain_name: str
    chat_size_max: int
    megagroup_size_max: int
    forwarded_count_max: int
    online_update_period_ms: int
    offline_blur_timeout_ms: int
    offline_idle_timeout_ms: int
    online_cloud_timeout_ms: int
    notify_cloud_delay_ms: int
    notify_default_delay_ms: int
    push_chat_period_ms: int
    push_chat_limit: int
    edit_time_limit: int
    revoke_time_limit: int
    revoke_pm_time_limit: int
    rating_e_decay: int
    stickers_recent_limit: int
    channels_read_media_period: int
    tmp_sessions: int | None
    call_receive_timeout_ms: int
    call_ring_timeout_ms: int
    call_connect_timeout_ms: int
    call_packet_timeout_ms: int
    me_url_prefix: str
    autoupdate_url_prefix: str | None
    gif_search_username: str | None
    venue_search_username: str | None
    img_search_username: str | None
    static_maps_provider: str | None
    caption_length_max: int
    message_length_max: int
    webfile_dc_id: int
    suggested_lang_code: str | None
    lang_pack_version: int | None
    base_lang_pack_version: int | None
    reactions_default: TLObject | None
    autologin_token: str | None
    def __init__(self, *, default_p2p_contacts: bool = ..., preload_featured_stickers: bool = ..., revoke_pm_inbox: bool = ..., blocked_mode: bool = ..., force_try_ipv6: bool = ..., date: int, expires: int, test_mode: bool, this_dc: int, dc_options: list[TLObject], dc_txt_domain_name: str, chat_size_max: int, megagroup_size_max: int, forwarded_count_max: int, online_update_period_ms: int, offline_blur_timeout_ms: int, offline_idle_timeout_ms: int, online_cloud_timeout_ms: int, notify_cloud_delay_ms: int, notify_default_delay_ms: int, push_chat_period_ms: int, push_chat_limit: int, edit_time_limit: int, revoke_time_limit: int, revoke_pm_time_limit: int, rating_e_decay: int, stickers_recent_limit: int, channels_read_media_period: int, tmp_sessions: int | None = ..., call_receive_timeout_ms: int, call_ring_timeout_ms: int, call_connect_timeout_ms: int, call_packet_timeout_ms: int, me_url_prefix: str, autoupdate_url_prefix: str | None = ..., gif_search_username: str | None = ..., venue_search_username: str | None = ..., img_search_username: str | None = ..., static_maps_provider: str | None = ..., caption_length_max: int, message_length_max: int, webfile_dc_id: int, suggested_lang_code: str | None = ..., lang_pack_version: int | None = ..., base_lang_pack_version: int | None = ..., reactions_default: TLObject | None = ..., autologin_token: str | None = ...) -> None: ...

class connectedBot(TLObject):
    bot_id: int
    recipients: TLObject
    rights: TLObject
    device: str | None
    date: int | None
    location: str | None
    def __init__(self, *, bot_id: int, recipients: TLObject, rights: TLObject, device: str | None = ..., date: int | None = ..., location: str | None = ...) -> None: ...

class connectedBotStarRef(TLObject):
    revoked: bool
    url: str
    date: int
    bot_id: int
    commission_permille: int
    duration_months: int | None
    participants: int
    revenue: int
    def __init__(self, *, revoked: bool = ..., url: str, date: int, bot_id: int, commission_permille: int, duration_months: int | None = ..., participants: int, revenue: int) -> None: ...

class contact(TLObject):
    user_id: int
    mutual: bool
    def __init__(self, *, user_id: int, mutual: bool) -> None: ...

class contactBirthday(TLObject):
    contact_id: int
    birthday: TLObject
    def __init__(self, *, contact_id: int, birthday: TLObject) -> None: ...

class contactStatus(TLObject):
    user_id: int
    status: TLObject
    def __init__(self, *, user_id: int, status: TLObject) -> None: ...

class contacts:
    class acceptContact(TLObject):
        id: TLObject
        def __init__(self, *, id: TLObject) -> None: ...

    class addContact(TLObject):
        add_phone_privacy_exception: bool
        id: TLObject
        first_name: str
        last_name: str
        phone: str
        note: TLObject | None
        def __init__(self, *, add_phone_privacy_exception: bool = ..., id: TLObject, first_name: str, last_name: str, phone: str, note: TLObject | None = ...) -> None: ...

    class block(TLObject):
        my_stories_from: bool
        id: TLObject
        def __init__(self, *, my_stories_from: bool = ..., id: TLObject) -> None: ...

    class blockFromReplies(TLObject):
        delete_message: bool
        delete_history: bool
        report_spam: bool
        msg_id: int
        def __init__(self, *, delete_message: bool = ..., delete_history: bool = ..., report_spam: bool = ..., msg_id: int) -> None: ...

    class blocked(TLObject):
        blocked: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, blocked: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class blockedSlice(TLObject):
        count: int
        blocked: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, blocked: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class contactBirthdays(TLObject):
        contacts: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, contacts: list[TLObject], users: list[TLObject]) -> None: ...

    class contacts(TLObject):
        contacts: list[TLObject]
        saved_count: int
        users: list[TLObject]
        def __init__(self, *, contacts: list[TLObject], saved_count: int, users: list[TLObject]) -> None: ...

    class contactsNotModified(TLObject):
        def __init__(self) -> None: ...

    class deleteByPhones(TLObject):
        phones: list[str]
        def __init__(self, *, phones: list[str]) -> None: ...

    class deleteContacts(TLObject):
        id: list[TLObject]
        def __init__(self, *, id: list[TLObject]) -> None: ...

    class editCloseFriends(TLObject):
        id: list[int]
        def __init__(self, *, id: list[int]) -> None: ...

    class exportContactToken(TLObject):
        def __init__(self) -> None: ...

    class exportNoPaidMessagesToken(TLObject):
        revoke: bool
        temporary: bool
        def __init__(self, *, revoke: bool = ..., temporary: bool = ...) -> None: ...

    class found(TLObject):
        my_results: list[TLObject]
        results: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, my_results: list[TLObject], results: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class getBirthdays(TLObject):
        def __init__(self) -> None: ...

    class getBlocked(TLObject):
        my_stories_from: bool
        offset: int
        limit: int
        def __init__(self, *, my_stories_from: bool = ..., offset: int, limit: int) -> None: ...

    class getContactIDs(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getContacts(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getLocated(TLObject):
        background: bool
        geo_point: TLObject
        self_expires: int | None
        def __init__(self, *, background: bool = ..., geo_point: TLObject, self_expires: int | None = ...) -> None: ...

    class getSaved(TLObject):
        def __init__(self) -> None: ...

    class getSponsoredPeers(TLObject):
        q: str
        def __init__(self, *, q: str) -> None: ...

    class getStatuses(TLObject):
        def __init__(self) -> None: ...

    class getTopPeers(TLObject):
        correspondents: bool
        bots_pm: bool
        bots_inline: bool
        phone_calls: bool
        forward_users: bool
        forward_chats: bool
        groups: bool
        channels: bool
        bots_app: bool
        bots_guestchat: bool
        offset: int
        limit: int
        hash: int
        def __init__(self, *, correspondents: bool = ..., bots_pm: bool = ..., bots_inline: bool = ..., phone_calls: bool = ..., forward_users: bool = ..., forward_chats: bool = ..., groups: bool = ..., channels: bool = ..., bots_app: bool = ..., bots_guestchat: bool = ..., offset: int, limit: int, hash: int) -> None: ...

    class importContactToken(TLObject):
        token: str
        def __init__(self, *, token: str) -> None: ...

    class importContacts(TLObject):
        contacts: list[TLObject]
        def __init__(self, *, contacts: list[TLObject]) -> None: ...

    class importNoPaidMessagesToken(TLObject):
        user_id: TLObject
        token: str
        def __init__(self, *, user_id: TLObject, token: str) -> None: ...

    class importedContacts(TLObject):
        imported: list[TLObject]
        popular_invites: list[TLObject]
        retry_contacts: list[int]
        users: list[TLObject]
        def __init__(self, *, imported: list[TLObject], popular_invites: list[TLObject], retry_contacts: list[int], users: list[TLObject]) -> None: ...

    class resetSaved(TLObject):
        def __init__(self) -> None: ...

    class resetTopPeerRating(TLObject):
        category: TLObject
        peer: TLObject
        def __init__(self, *, category: TLObject, peer: TLObject) -> None: ...

    class resolvePhone(TLObject):
        phone: str
        def __init__(self, *, phone: str) -> None: ...

    class resolveUsername(TLObject):
        username: str
        referer: str | None
        def __init__(self, *, username: str, referer: str | None = ...) -> None: ...

    class resolvedPeer(TLObject):
        peer: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, peer: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class search(TLObject):
        broadcasts: bool
        bots: bool
        q: str
        limit: int
        def __init__(self, *, broadcasts: bool = ..., bots: bool = ..., q: str, limit: int) -> None: ...

    class setBlocked(TLObject):
        my_stories_from: bool
        id: list[TLObject]
        limit: int
        def __init__(self, *, my_stories_from: bool = ..., id: list[TLObject], limit: int) -> None: ...

    class sponsoredPeers(TLObject):
        peers: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, peers: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class sponsoredPeersEmpty(TLObject):
        def __init__(self) -> None: ...

    class toggleTopPeers(TLObject):
        enabled: bool
        def __init__(self, *, enabled: bool) -> None: ...

    class topPeers(TLObject):
        categories: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, categories: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class topPeersDisabled(TLObject):
        def __init__(self) -> None: ...

    class topPeersNotModified(TLObject):
        def __init__(self) -> None: ...

    class unblock(TLObject):
        my_stories_from: bool
        id: TLObject
        def __init__(self, *, my_stories_from: bool = ..., id: TLObject) -> None: ...

    class updateContactNote(TLObject):
        id: TLObject
        note: TLObject
        def __init__(self, *, id: TLObject, note: TLObject) -> None: ...

class currencyRate(TLObject):
    currency: str
    rate: float
    def __init__(self, *, currency: str, rate: float) -> None: ...

class dataJSON(TLObject):
    data: str
    def __init__(self, *, data: str) -> None: ...

class dcOption(TLObject):
    ipv6: bool
    media_only: bool
    tcpo_only: bool
    cdn: bool
    static: bool
    this_port_only: bool
    id: int
    ip_address: str
    port: int
    secret: bytes | None
    def __init__(self, *, ipv6: bool = ..., media_only: bool = ..., tcpo_only: bool = ..., cdn: bool = ..., static: bool = ..., this_port_only: bool = ..., id: int, ip_address: str, port: int, secret: bytes | None = ...) -> None: ...

class defaultHistoryTTL(TLObject):
    period: int
    def __init__(self, *, period: int) -> None: ...

class dialog(TLObject):
    pinned: bool
    unread_mark: bool
    view_forum_as_messages: bool
    peer: TLObject
    top_message: int
    read_inbox_max_id: int
    read_outbox_max_id: int
    unread_count: int
    unread_mentions_count: int
    unread_reactions_count: int
    unread_poll_votes_count: int
    notify_settings: TLObject
    pts: int | None
    draft: TLObject | None
    folder_id: int | None
    ttl_period: int | None
    def __init__(self, *, pinned: bool = ..., unread_mark: bool = ..., view_forum_as_messages: bool = ..., peer: TLObject, top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_mentions_count: int, unread_reactions_count: int, unread_poll_votes_count: int, notify_settings: TLObject, pts: int | None = ..., draft: TLObject | None = ..., folder_id: int | None = ..., ttl_period: int | None = ...) -> None: ...

class dialogCommunity(TLObject):
    pinned: bool
    community_id: int
    notify_settings: TLObject
    def __init__(self, *, pinned: bool = ..., community_id: int, notify_settings: TLObject) -> None: ...

class dialogFilter(TLObject):
    contacts: bool
    non_contacts: bool
    groups: bool
    broadcasts: bool
    bots: bool
    exclude_muted: bool
    exclude_read: bool
    exclude_archived: bool
    title_noanimate: bool
    id: int
    title: TLObject
    emoticon: str | None
    color: int | None
    pinned_peers: list[TLObject]
    include_peers: list[TLObject]
    exclude_peers: list[TLObject]
    def __init__(self, *, contacts: bool = ..., non_contacts: bool = ..., groups: bool = ..., broadcasts: bool = ..., bots: bool = ..., exclude_muted: bool = ..., exclude_read: bool = ..., exclude_archived: bool = ..., title_noanimate: bool = ..., id: int, title: TLObject, emoticon: str | None = ..., color: int | None = ..., pinned_peers: list[TLObject], include_peers: list[TLObject], exclude_peers: list[TLObject]) -> None: ...

class dialogFilterChatlist(TLObject):
    has_my_invites: bool
    title_noanimate: bool
    id: int
    title: TLObject
    emoticon: str | None
    color: int | None
    pinned_peers: list[TLObject]
    include_peers: list[TLObject]
    def __init__(self, *, has_my_invites: bool = ..., title_noanimate: bool = ..., id: int, title: TLObject, emoticon: str | None = ..., color: int | None = ..., pinned_peers: list[TLObject], include_peers: list[TLObject]) -> None: ...

class dialogFilterDefault(TLObject):
    def __init__(self) -> None: ...

class dialogFilterSuggested(TLObject):
    filter: TLObject
    description: str
    def __init__(self, *, filter: TLObject, description: str) -> None: ...

class dialogFolder(TLObject):
    pinned: bool
    folder: TLObject
    peer: TLObject
    top_message: int
    unread_muted_peers_count: int
    unread_unmuted_peers_count: int
    unread_muted_messages_count: int
    unread_unmuted_messages_count: int
    def __init__(self, *, pinned: bool = ..., folder: TLObject, peer: TLObject, top_message: int, unread_muted_peers_count: int, unread_unmuted_peers_count: int, unread_muted_messages_count: int, unread_unmuted_messages_count: int) -> None: ...

class dialogPeer(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class dialogPeerCommunity(TLObject):
    community_id: int
    def __init__(self, *, community_id: int) -> None: ...

class dialogPeerFolder(TLObject):
    folder_id: int
    def __init__(self, *, folder_id: int) -> None: ...

class disallowedGiftsSettings(TLObject):
    disallow_unlimited_stargifts: bool
    disallow_limited_stargifts: bool
    disallow_unique_stargifts: bool
    disallow_premium_gifts: bool
    disallow_stargifts_from_channels: bool
    def __init__(self, *, disallow_unlimited_stargifts: bool = ..., disallow_limited_stargifts: bool = ..., disallow_unique_stargifts: bool = ..., disallow_premium_gifts: bool = ..., disallow_stargifts_from_channels: bool = ...) -> None: ...

class document(TLObject):
    id: int
    access_hash: int
    file_reference: bytes
    date: int
    mime_type: str
    size: int
    thumbs: list[TLObject] | None
    video_thumbs: list[TLObject] | None
    dc_id: int
    attributes: list[TLObject]
    def __init__(self, *, id: int, access_hash: int, file_reference: bytes, date: int, mime_type: str, size: int, thumbs: list[TLObject] | None = ..., video_thumbs: list[TLObject] | None = ..., dc_id: int, attributes: list[TLObject]) -> None: ...

class documentAttributeAnimated(TLObject):
    def __init__(self) -> None: ...

class documentAttributeAudio(TLObject):
    voice: bool
    duration: int
    title: str | None
    performer: str | None
    waveform: bytes | None
    def __init__(self, *, voice: bool = ..., duration: int, title: str | None = ..., performer: str | None = ..., waveform: bytes | None = ...) -> None: ...

class documentAttributeCustomEmoji(TLObject):
    free: bool
    text_color: bool
    alt: str
    stickerset: TLObject
    def __init__(self, *, free: bool = ..., text_color: bool = ..., alt: str, stickerset: TLObject) -> None: ...

class documentAttributeFilename(TLObject):
    file_name: str
    def __init__(self, *, file_name: str) -> None: ...

class documentAttributeHasStickers(TLObject):
    def __init__(self) -> None: ...

class documentAttributeImageSize(TLObject):
    w: int
    h: int
    def __init__(self, *, w: int, h: int) -> None: ...

class documentAttributeSticker(TLObject):
    mask: bool
    alt: str
    stickerset: TLObject
    mask_coords: TLObject | None
    def __init__(self, *, mask: bool = ..., alt: str, stickerset: TLObject, mask_coords: TLObject | None = ...) -> None: ...

class documentAttributeVideo(TLObject):
    round_message: bool
    supports_streaming: bool
    nosound: bool
    duration: float
    w: int
    h: int
    preload_prefix_size: int | None
    video_start_ts: float | None
    video_codec: str | None
    def __init__(self, *, round_message: bool = ..., supports_streaming: bool = ..., nosound: bool = ..., duration: float, w: int, h: int, preload_prefix_size: int | None = ..., video_start_ts: float | None = ..., video_codec: str | None = ...) -> None: ...

class documentEmpty(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class draftMessage(TLObject):
    no_webpage: bool
    invert_media: bool
    reply_to: TLObject | None
    message: str
    entities: list[TLObject] | None
    media: TLObject | None
    date: int
    effect: int | None
    suggested_post: TLObject | None
    rich_message: TLObject | None
    def __init__(self, *, no_webpage: bool = ..., invert_media: bool = ..., reply_to: TLObject | None = ..., message: str, entities: list[TLObject] | None = ..., media: TLObject | None = ..., date: int, effect: int | None = ..., suggested_post: TLObject | None = ..., rich_message: TLObject | None = ...) -> None: ...

class draftMessageEmpty(TLObject):
    date: int | None
    def __init__(self, *, date: int | None = ...) -> None: ...

class emailVerificationApple(TLObject):
    token: str
    def __init__(self, *, token: str) -> None: ...

class emailVerificationCode(TLObject):
    code: str
    def __init__(self, *, code: str) -> None: ...

class emailVerificationGoogle(TLObject):
    token: str
    def __init__(self, *, token: str) -> None: ...

class emailVerifyPurposeLoginChange(TLObject):
    def __init__(self) -> None: ...

class emailVerifyPurposeLoginSetup(TLObject):
    phone_number: str
    phone_code_hash: str
    def __init__(self, *, phone_number: str, phone_code_hash: str) -> None: ...

class emailVerifyPurposePassport(TLObject):
    def __init__(self) -> None: ...

class emojiGroup(TLObject):
    title: str
    icon_emoji_id: int
    emoticons: list[str]
    def __init__(self, *, title: str, icon_emoji_id: int, emoticons: list[str]) -> None: ...

class emojiGroupGreeting(TLObject):
    title: str
    icon_emoji_id: int
    emoticons: list[str]
    def __init__(self, *, title: str, icon_emoji_id: int, emoticons: list[str]) -> None: ...

class emojiGroupPremium(TLObject):
    title: str
    icon_emoji_id: int
    def __init__(self, *, title: str, icon_emoji_id: int) -> None: ...

class emojiKeyword(TLObject):
    keyword: str
    emoticons: list[str]
    def __init__(self, *, keyword: str, emoticons: list[str]) -> None: ...

class emojiKeywordDeleted(TLObject):
    keyword: str
    emoticons: list[str]
    def __init__(self, *, keyword: str, emoticons: list[str]) -> None: ...

class emojiKeywordsDifference(TLObject):
    lang_code: str
    from_version: int
    version: int
    keywords: list[TLObject]
    def __init__(self, *, lang_code: str, from_version: int, version: int, keywords: list[TLObject]) -> None: ...

class emojiLanguage(TLObject):
    lang_code: str
    def __init__(self, *, lang_code: str) -> None: ...

class emojiList(TLObject):
    hash: int
    document_id: list[int]
    def __init__(self, *, hash: int, document_id: list[int]) -> None: ...

class emojiListNotModified(TLObject):
    def __init__(self) -> None: ...

class emojiStatus(TLObject):
    document_id: int
    until: int | None
    def __init__(self, *, document_id: int, until: int | None = ...) -> None: ...

class emojiStatusCollectible(TLObject):
    collectible_id: int
    document_id: int
    title: str
    slug: str
    pattern_document_id: int
    center_color: int
    edge_color: int
    pattern_color: int
    text_color: int
    until: int | None
    def __init__(self, *, collectible_id: int, document_id: int, title: str, slug: str, pattern_document_id: int, center_color: int, edge_color: int, pattern_color: int, text_color: int, until: int | None = ...) -> None: ...

class emojiStatusEmpty(TLObject):
    def __init__(self) -> None: ...

class emojiURL(TLObject):
    url: str
    def __init__(self, *, url: str) -> None: ...

class encryptedChat(TLObject):
    id: int
    access_hash: int
    date: int
    admin_id: int
    participant_id: int
    g_a_or_b: bytes
    key_fingerprint: int
    def __init__(self, *, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_or_b: bytes, key_fingerprint: int) -> None: ...

class encryptedChatDiscarded(TLObject):
    history_deleted: bool
    id: int
    def __init__(self, *, history_deleted: bool = ..., id: int) -> None: ...

class encryptedChatEmpty(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class encryptedChatRequested(TLObject):
    folder_id: int | None
    id: int
    access_hash: int
    date: int
    admin_id: int
    participant_id: int
    g_a: bytes
    def __init__(self, *, folder_id: int | None = ..., id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a: bytes) -> None: ...

class encryptedChatWaiting(TLObject):
    id: int
    access_hash: int
    date: int
    admin_id: int
    participant_id: int
    def __init__(self, *, id: int, access_hash: int, date: int, admin_id: int, participant_id: int) -> None: ...

class encryptedFile(TLObject):
    id: int
    access_hash: int
    size: int
    dc_id: int
    key_fingerprint: int
    def __init__(self, *, id: int, access_hash: int, size: int, dc_id: int, key_fingerprint: int) -> None: ...

class encryptedFileEmpty(TLObject):
    def __init__(self) -> None: ...

class encryptedMessage(TLObject):
    random_id: int
    chat_id: int
    date: int
    bytes: bytes
    file: TLObject
    def __init__(self, *, random_id: int, chat_id: int, date: int, bytes: bytes, file: TLObject) -> None: ...

class encryptedMessageService(TLObject):
    random_id: int
    chat_id: int
    date: int
    bytes: bytes
    def __init__(self, *, random_id: int, chat_id: int, date: int, bytes: bytes) -> None: ...

class ephemeral:
    class deleteAllWelcomeMessages(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class deleteMessage(TLObject):
        peer: TLObject | None
        receiver_id: TLObject
        id: int
        def __init__(self, *, peer: TLObject | None = ..., receiver_id: TLObject, id: int) -> None: ...

    class deleteWelcomeMessage(TLObject):
        peer: TLObject
        id: int
        def __init__(self, *, peer: TLObject, id: int) -> None: ...

    class editMessage(TLObject):
        invert_media: bool
        welcome: bool
        peer: TLObject | None
        receiver_id: TLObject
        id: int
        message: str | None
        media: TLObject | None
        entities: list[TLObject] | None
        reply_markup: TLObject | None
        rich_message: TLObject | None
        def __init__(self, *, invert_media: bool = ..., welcome: bool = ..., peer: TLObject | None = ..., receiver_id: TLObject, id: int, message: str | None = ..., media: TLObject | None = ..., entities: list[TLObject] | None = ..., reply_markup: TLObject | None = ..., rich_message: TLObject | None = ...) -> None: ...

    class getCallbackAnswer(TLObject):
        peer: TLObject
        id: int
        data: bytes | None
        def __init__(self, *, peer: TLObject, id: int, data: bytes | None = ...) -> None: ...

    class getWelcomeMessages(TLObject):
        peer: TLObject
        hash: int
        def __init__(self, *, peer: TLObject, hash: int) -> None: ...

    class reportMessage(TLObject):
        peer: TLObject
        id: int
        option: bytes
        message: str
        def __init__(self, *, peer: TLObject, id: int, option: bytes, message: str) -> None: ...

    class sendMessage(TLObject):
        invert_media: bool
        welcome: bool
        anchor: bool
        noforwards: bool
        peer: TLObject | None
        receiver_id: TLObject
        query_id: int | None
        message: str
        entities: list[TLObject] | None
        media: TLObject | None
        reply_markup: TLObject | None
        rich_message: TLObject | None
        random_id: int
        reply_to: TLObject | None
        def __init__(self, *, invert_media: bool = ..., welcome: bool = ..., anchor: bool = ..., noforwards: bool = ..., peer: TLObject | None = ..., receiver_id: TLObject, query_id: int | None = ..., message: str, entities: list[TLObject] | None = ..., media: TLObject | None = ..., reply_markup: TLObject | None = ..., rich_message: TLObject | None = ..., random_id: int, reply_to: TLObject | None = ...) -> None: ...

    class welcomeMessages(TLObject):
        hash: int
        messages: list[TLObject]
        def __init__(self, *, hash: int, messages: list[TLObject]) -> None: ...

    class welcomeMessagesNotModified(TLObject):
        def __init__(self) -> None: ...

class ephemeralMessage(TLObject):
    out: bool
    welcome_template: bool
    invert_media: bool
    noforwards: bool
    id: int
    from_id: TLObject
    peer_id: TLObject | None
    receiver_id: int
    top_msg_id: int | None
    date: int
    message: str
    entities: list[TLObject] | None
    media: TLObject | None
    reply_markup: TLObject | None
    reply_to: TLObject | None
    rich_message: TLObject | None
    chat_instance: int | None
    anchor_msg_id: int | None
    def __init__(self, *, out: bool = ..., welcome_template: bool = ..., invert_media: bool = ..., noforwards: bool = ..., id: int, from_id: TLObject, peer_id: TLObject | None = ..., receiver_id: int, top_msg_id: int | None = ..., date: int, message: str, entities: list[TLObject] | None = ..., media: TLObject | None = ..., reply_markup: TLObject | None = ..., reply_to: TLObject | None = ..., rich_message: TLObject | None = ..., chat_instance: int | None = ..., anchor_msg_id: int | None = ...) -> None: ...

class error(TLObject):
    code: int
    text: str
    def __init__(self, *, code: int, text: str) -> None: ...

class exportedChatlistInvite(TLObject):
    title: str
    url: str
    peers: list[TLObject]
    def __init__(self, *, title: str, url: str, peers: list[TLObject]) -> None: ...

class exportedContactToken(TLObject):
    url: str
    expires: int
    def __init__(self, *, url: str, expires: int) -> None: ...

class exportedMessageLink(TLObject):
    link: str
    html: str
    def __init__(self, *, link: str, html: str) -> None: ...

class exportedNoPaidMessagesToken(TLObject):
    token: str
    url: str
    expires: int | None
    def __init__(self, *, token: str, url: str, expires: int | None = ...) -> None: ...

class exportedStoryLink(TLObject):
    link: str
    def __init__(self, *, link: str) -> None: ...

class factCheck(TLObject):
    need_check: bool
    country: str | None
    text: TLObject | None
    hash: int
    def __init__(self, *, need_check: bool = ..., country: str | None = ..., text: TLObject | None = ..., hash: int) -> None: ...

class fileHash(TLObject):
    offset: int
    limit: int
    hash: bytes
    def __init__(self, *, offset: int, limit: int, hash: bytes) -> None: ...

class folder(TLObject):
    autofill_new_broadcasts: bool
    autofill_public_groups: bool
    autofill_new_correspondents: bool
    id: int
    title: str
    photo: TLObject | None
    def __init__(self, *, autofill_new_broadcasts: bool = ..., autofill_public_groups: bool = ..., autofill_new_correspondents: bool = ..., id: int, title: str, photo: TLObject | None = ...) -> None: ...

class folderPeer(TLObject):
    peer: TLObject
    folder_id: int
    def __init__(self, *, peer: TLObject, folder_id: int) -> None: ...

class folders:
    class editPeerFolders(TLObject):
        folder_peers: list[TLObject]
        def __init__(self, *, folder_peers: list[TLObject]) -> None: ...

class forumTopic(TLObject):
    my: bool
    closed: bool
    pinned: bool
    short: bool
    hidden: bool
    title_missing: bool
    id: int
    date: int
    peer: TLObject
    title: str
    icon_color: int
    icon_emoji_id: int | None
    top_message: int
    read_inbox_max_id: int
    read_outbox_max_id: int
    unread_count: int
    unread_mentions_count: int
    unread_reactions_count: int
    unread_poll_votes_count: int
    from_id: TLObject
    notify_settings: TLObject
    draft: TLObject | None
    def __init__(self, *, my: bool = ..., closed: bool = ..., pinned: bool = ..., short: bool = ..., hidden: bool = ..., title_missing: bool = ..., id: int, date: int, peer: TLObject, title: str, icon_color: int, icon_emoji_id: int | None = ..., top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_mentions_count: int, unread_reactions_count: int, unread_poll_votes_count: int, from_id: TLObject, notify_settings: TLObject, draft: TLObject | None = ...) -> None: ...

class forumTopicDeleted(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class foundStory(TLObject):
    peer: TLObject
    story: TLObject
    def __init__(self, *, peer: TLObject, story: TLObject) -> None: ...

class fragment:
    class collectibleInfo(TLObject):
        purchase_date: int
        currency: str
        amount: int
        crypto_currency: str
        crypto_amount: int
        url: str
        def __init__(self, *, purchase_date: int, currency: str, amount: int, crypto_currency: str, crypto_amount: int, url: str) -> None: ...

    class getCollectibleInfo(TLObject):
        collectible: TLObject
        def __init__(self, *, collectible: TLObject) -> None: ...

class game(TLObject):
    id: int
    access_hash: int
    short_name: str
    title: str
    description: str
    photo: TLObject
    document: TLObject | None
    def __init__(self, *, id: int, access_hash: int, short_name: str, title: str, description: str, photo: TLObject, document: TLObject | None = ...) -> None: ...

class geoPoint(TLObject):
    long: float
    lat: float
    access_hash: int
    accuracy_radius: int | None
    def __init__(self, *, long: float, lat: float, access_hash: int, accuracy_radius: int | None = ...) -> None: ...

class geoPointAddress(TLObject):
    country_iso2: str
    state: str | None
    city: str | None
    street: str | None
    def __init__(self, *, country_iso2: str, state: str | None = ..., city: str | None = ..., street: str | None = ...) -> None: ...

class geoPointEmpty(TLObject):
    def __init__(self) -> None: ...

class globalPrivacySettings(TLObject):
    archive_and_mute_new_noncontact_peers: bool
    keep_archived_unmuted: bool
    keep_archived_folders: bool
    hide_read_marks: bool
    new_noncontact_peers_require_premium: bool
    display_gifts_button: bool
    noncontact_peers_paid_stars: int | None
    disallowed_gifts: TLObject | None
    def __init__(self, *, archive_and_mute_new_noncontact_peers: bool = ..., keep_archived_unmuted: bool = ..., keep_archived_folders: bool = ..., hide_read_marks: bool = ..., new_noncontact_peers_require_premium: bool = ..., display_gifts_button: bool = ..., noncontact_peers_paid_stars: int | None = ..., disallowed_gifts: TLObject | None = ...) -> None: ...

class groupCall(TLObject):
    join_muted: bool
    can_change_join_muted: bool
    join_date_asc: bool
    schedule_start_subscribed: bool
    can_start_video: bool
    record_video_active: bool
    rtmp_stream: bool
    listeners_hidden: bool
    conference: bool
    creator: bool
    messages_enabled: bool
    can_change_messages_enabled: bool
    min: bool
    id: int
    access_hash: int
    participants_count: int
    title: str | None
    stream_dc_id: int | None
    record_start_date: int | None
    schedule_date: int | None
    unmuted_video_count: int | None
    unmuted_video_limit: int
    version: int
    invite_link: str | None
    send_paid_messages_stars: int | None
    default_send_as: TLObject | None
    def __init__(self, *, join_muted: bool = ..., can_change_join_muted: bool = ..., join_date_asc: bool = ..., schedule_start_subscribed: bool = ..., can_start_video: bool = ..., record_video_active: bool = ..., rtmp_stream: bool = ..., listeners_hidden: bool = ..., conference: bool = ..., creator: bool = ..., messages_enabled: bool = ..., can_change_messages_enabled: bool = ..., min: bool = ..., id: int, access_hash: int, participants_count: int, title: str | None = ..., stream_dc_id: int | None = ..., record_start_date: int | None = ..., schedule_date: int | None = ..., unmuted_video_count: int | None = ..., unmuted_video_limit: int, version: int, invite_link: str | None = ..., send_paid_messages_stars: int | None = ..., default_send_as: TLObject | None = ...) -> None: ...

class groupCallDiscarded(TLObject):
    id: int
    access_hash: int
    duration: int
    def __init__(self, *, id: int, access_hash: int, duration: int) -> None: ...

class groupCallDonor(TLObject):
    top: bool
    my: bool
    peer_id: TLObject | None
    stars: int
    def __init__(self, *, top: bool = ..., my: bool = ..., peer_id: TLObject | None = ..., stars: int) -> None: ...

class groupCallMessage(TLObject):
    from_admin: bool
    id: int
    from_id: TLObject
    date: int
    message: TLObject
    paid_message_stars: int | None
    def __init__(self, *, from_admin: bool = ..., id: int, from_id: TLObject, date: int, message: TLObject, paid_message_stars: int | None = ...) -> None: ...

class groupCallParticipant(TLObject):
    muted: bool
    left: bool
    can_self_unmute: bool
    just_joined: bool
    versioned: bool
    min: bool
    muted_by_you: bool
    volume_by_admin: bool
    self_: bool
    video_joined: bool
    peer: TLObject
    date: int
    active_date: int | None
    source: int
    volume: int | None
    about: str | None
    raise_hand_rating: int | None
    video: TLObject | None
    presentation: TLObject | None
    paid_stars_total: int | None
    def __init__(self, *, muted: bool = ..., left: bool = ..., can_self_unmute: bool = ..., just_joined: bool = ..., versioned: bool = ..., min: bool = ..., muted_by_you: bool = ..., volume_by_admin: bool = ..., self_: bool = ..., video_joined: bool = ..., peer: TLObject, date: int, active_date: int | None = ..., source: int, volume: int | None = ..., about: str | None = ..., raise_hand_rating: int | None = ..., video: TLObject | None = ..., presentation: TLObject | None = ..., paid_stars_total: int | None = ...) -> None: ...

class groupCallParticipantVideo(TLObject):
    paused: bool
    endpoint: str
    source_groups: list[TLObject]
    audio_source: int | None
    def __init__(self, *, paused: bool = ..., endpoint: str, source_groups: list[TLObject], audio_source: int | None = ...) -> None: ...

class groupCallParticipantVideoSourceGroup(TLObject):
    semantics: str
    sources: list[int]
    def __init__(self, *, semantics: str, sources: list[int]) -> None: ...

class groupCallStreamChannel(TLObject):
    channel: int
    scale: int
    last_timestamp_ms: int
    def __init__(self, *, channel: int, scale: int, last_timestamp_ms: int) -> None: ...

class help:
    class acceptTermsOfService(TLObject):
        id: TLObject
        def __init__(self, *, id: TLObject) -> None: ...

    class appConfig(TLObject):
        hash: int
        config: TLObject
        def __init__(self, *, hash: int, config: TLObject) -> None: ...

    class appConfigNotModified(TLObject):
        def __init__(self) -> None: ...

    class appUpdate(TLObject):
        can_not_skip: bool
        id: int
        version: str
        text: str
        entities: list[TLObject]
        document: TLObject | None
        url: str | None
        sticker: TLObject | None
        def __init__(self, *, can_not_skip: bool = ..., id: int, version: str, text: str, entities: list[TLObject], document: TLObject | None = ..., url: str | None = ..., sticker: TLObject | None = ...) -> None: ...

    class countriesList(TLObject):
        countries: list[TLObject]
        hash: int
        def __init__(self, *, countries: list[TLObject], hash: int) -> None: ...

    class countriesListNotModified(TLObject):
        def __init__(self) -> None: ...

    class country(TLObject):
        hidden: bool
        iso2: str
        default_name: str
        name: str | None
        country_codes: list[TLObject]
        def __init__(self, *, hidden: bool = ..., iso2: str, default_name: str, name: str | None = ..., country_codes: list[TLObject]) -> None: ...

    class countryCode(TLObject):
        country_code: str
        prefixes: list[str] | None
        patterns: list[str] | None
        def __init__(self, *, country_code: str, prefixes: list[str] | None = ..., patterns: list[str] | None = ...) -> None: ...

    class deepLinkInfo(TLObject):
        update_app: bool
        message: str
        entities: list[TLObject] | None
        def __init__(self, *, update_app: bool = ..., message: str, entities: list[TLObject] | None = ...) -> None: ...

    class deepLinkInfoEmpty(TLObject):
        def __init__(self) -> None: ...

    class dismissSuggestion(TLObject):
        peer: TLObject
        suggestion: str
        def __init__(self, *, peer: TLObject, suggestion: str) -> None: ...

    class editUserInfo(TLObject):
        user_id: TLObject
        message: str
        entities: list[TLObject]
        def __init__(self, *, user_id: TLObject, message: str, entities: list[TLObject]) -> None: ...

    class getAppConfig(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getAppUpdate(TLObject):
        source: str
        def __init__(self, *, source: str) -> None: ...

    class getCdnConfig(TLObject):
        def __init__(self) -> None: ...

    class getConfig(TLObject):
        def __init__(self) -> None: ...

    class getCountriesList(TLObject):
        lang_code: str
        hash: int
        def __init__(self, *, lang_code: str, hash: int) -> None: ...

    class getDeepLinkInfo(TLObject):
        path: str
        def __init__(self, *, path: str) -> None: ...

    class getInviteText(TLObject):
        def __init__(self) -> None: ...

    class getNearestDc(TLObject):
        def __init__(self) -> None: ...

    class getPassportConfig(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getPeerColors(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getPeerProfileColors(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getPremiumPromo(TLObject):
        def __init__(self) -> None: ...

    class getPromoData(TLObject):
        def __init__(self) -> None: ...

    class getRecentMeUrls(TLObject):
        referer: str
        def __init__(self, *, referer: str) -> None: ...

    class getSupport(TLObject):
        def __init__(self) -> None: ...

    class getSupportName(TLObject):
        def __init__(self) -> None: ...

    class getTermsOfServiceUpdate(TLObject):
        def __init__(self) -> None: ...

    class getTimezonesList(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getUserInfo(TLObject):
        user_id: TLObject
        def __init__(self, *, user_id: TLObject) -> None: ...

    class hidePromoData(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class inviteText(TLObject):
        message: str
        def __init__(self, *, message: str) -> None: ...

    class noAppUpdate(TLObject):
        def __init__(self) -> None: ...

    class passportConfig(TLObject):
        hash: int
        countries_langs: TLObject
        def __init__(self, *, hash: int, countries_langs: TLObject) -> None: ...

    class passportConfigNotModified(TLObject):
        def __init__(self) -> None: ...

    class peerColorOption(TLObject):
        hidden: bool
        color_id: int
        colors: TLObject | None
        dark_colors: TLObject | None
        channel_min_level: int | None
        group_min_level: int | None
        def __init__(self, *, hidden: bool = ..., color_id: int, colors: TLObject | None = ..., dark_colors: TLObject | None = ..., channel_min_level: int | None = ..., group_min_level: int | None = ...) -> None: ...

    class peerColorProfileSet(TLObject):
        palette_colors: list[int]
        bg_colors: list[int]
        story_colors: list[int]
        def __init__(self, *, palette_colors: list[int], bg_colors: list[int], story_colors: list[int]) -> None: ...

    class peerColorSet(TLObject):
        colors: list[int]
        def __init__(self, *, colors: list[int]) -> None: ...

    class peerColors(TLObject):
        hash: int
        colors: list[TLObject]
        def __init__(self, *, hash: int, colors: list[TLObject]) -> None: ...

    class peerColorsNotModified(TLObject):
        def __init__(self) -> None: ...

    class premiumPromo(TLObject):
        status_text: str
        status_entities: list[TLObject]
        video_sections: list[str]
        videos: list[TLObject]
        period_options: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, status_text: str, status_entities: list[TLObject], video_sections: list[str], videos: list[TLObject], period_options: list[TLObject], users: list[TLObject]) -> None: ...

    class promoData(TLObject):
        proxy: bool
        expires: int
        peer: TLObject | None
        psa_type: str | None
        psa_message: str | None
        pending_suggestions: list[str]
        dismissed_suggestions: list[str]
        custom_pending_suggestion: TLObject | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, proxy: bool = ..., expires: int, peer: TLObject | None = ..., psa_type: str | None = ..., psa_message: str | None = ..., pending_suggestions: list[str], dismissed_suggestions: list[str], custom_pending_suggestion: TLObject | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class promoDataEmpty(TLObject):
        expires: int
        def __init__(self, *, expires: int) -> None: ...

    class recentMeUrls(TLObject):
        urls: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, urls: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class saveAppLog(TLObject):
        events: list[TLObject]
        def __init__(self, *, events: list[TLObject]) -> None: ...

    class setBotUpdatesStatus(TLObject):
        pending_updates_count: int
        message: str
        def __init__(self, *, pending_updates_count: int, message: str) -> None: ...

    class support(TLObject):
        phone_number: str
        user: TLObject
        def __init__(self, *, phone_number: str, user: TLObject) -> None: ...

    class supportName(TLObject):
        name: str
        def __init__(self, *, name: str) -> None: ...

    class termsOfService(TLObject):
        popup: bool
        id: TLObject
        text: str
        entities: list[TLObject]
        min_age_confirm: int | None
        def __init__(self, *, popup: bool = ..., id: TLObject, text: str, entities: list[TLObject], min_age_confirm: int | None = ...) -> None: ...

    class termsOfServiceUpdate(TLObject):
        expires: int
        terms_of_service: TLObject
        def __init__(self, *, expires: int, terms_of_service: TLObject) -> None: ...

    class termsOfServiceUpdateEmpty(TLObject):
        expires: int
        def __init__(self, *, expires: int) -> None: ...

    class timezonesList(TLObject):
        timezones: list[TLObject]
        hash: int
        def __init__(self, *, timezones: list[TLObject], hash: int) -> None: ...

    class timezonesListNotModified(TLObject):
        def __init__(self) -> None: ...

    class userInfo(TLObject):
        message: str
        entities: list[TLObject]
        author: str
        date: int
        def __init__(self, *, message: str, entities: list[TLObject], author: str, date: int) -> None: ...

    class userInfoEmpty(TLObject):
        def __init__(self) -> None: ...

class highScore(TLObject):
    pos: int
    user_id: int
    score: int
    def __init__(self, *, pos: int, user_id: int, score: int) -> None: ...

class importedContact(TLObject):
    user_id: int
    client_id: int
    def __init__(self, *, user_id: int, client_id: int) -> None: ...

class initConnection(TLObject):
    api_id: int
    device_model: str
    system_version: str
    app_version: str
    system_lang_code: str
    lang_pack: str
    lang_code: str
    proxy: TLObject | None
    params: TLObject | None
    query: TLObject
    def __init__(self, *, api_id: int, device_model: str, system_version: str, app_version: str, system_lang_code: str, lang_pack: str, lang_code: str, proxy: TLObject | None = ..., params: TLObject | None = ..., query: TLObject) -> None: ...

class inlineBotSwitchPM(TLObject):
    text: str
    start_param: str
    def __init__(self, *, text: str, start_param: str) -> None: ...

class inlineBotWebView(TLObject):
    text: str
    url: str
    def __init__(self, *, text: str, url: str) -> None: ...

class inlineButtonTypeBuy(TLObject):
    def __init__(self) -> None: ...

class inlineButtonTypeCallback(TLObject):
    requires_password: bool
    data: bytes
    def __init__(self, *, requires_password: bool = ..., data: bytes) -> None: ...

class inlineButtonTypeCopy(TLObject):
    copy_text: str
    def __init__(self, *, copy_text: str) -> None: ...

class inlineButtonTypeDisabled(TLObject):
    def __init__(self) -> None: ...

class inlineButtonTypeGame(TLObject):
    def __init__(self) -> None: ...

class inlineButtonTypeSwitchInline(TLObject):
    same_peer: bool
    query: str
    peer_types: list[TLObject] | None
    def __init__(self, *, same_peer: bool = ..., query: str, peer_types: list[TLObject] | None = ...) -> None: ...

class inlineButtonTypeUrl(TLObject):
    url: str
    def __init__(self, *, url: str) -> None: ...

class inlineButtonTypeUrlAuth(TLObject):
    fwd_text: str | None
    url: str
    button_id: int
    def __init__(self, *, fwd_text: str | None = ..., url: str, button_id: int) -> None: ...

class inlineButtonTypeUserProfile(TLObject):
    user_id: int
    def __init__(self, *, user_id: int) -> None: ...

class inlineButtonTypeWebView(TLObject):
    url: str
    def __init__(self, *, url: str) -> None: ...

class inlineQueryPeerTypeBotPM(TLObject):
    def __init__(self) -> None: ...

class inlineQueryPeerTypeBroadcast(TLObject):
    def __init__(self) -> None: ...

class inlineQueryPeerTypeChat(TLObject):
    def __init__(self) -> None: ...

class inlineQueryPeerTypeMegagroup(TLObject):
    def __init__(self) -> None: ...

class inlineQueryPeerTypePM(TLObject):
    def __init__(self) -> None: ...

class inlineQueryPeerTypeSameBotPM(TLObject):
    def __init__(self) -> None: ...

class inputAiComposeToneDefault(TLObject):
    tone: str
    def __init__(self, *, tone: str) -> None: ...

class inputAiComposeToneID(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputAiComposeToneSingleUse(TLObject):
    custom_prompt: str
    def __init__(self, *, custom_prompt: str) -> None: ...

class inputAiComposeToneSlug(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class inputAppEvent(TLObject):
    time: float
    type: str
    peer: int
    data: TLObject
    def __init__(self, *, time: float, type: str, peer: int, data: TLObject) -> None: ...

class inputBotAppID(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputBotAppShortName(TLObject):
    bot_id: TLObject
    short_name: str
    def __init__(self, *, bot_id: TLObject, short_name: str) -> None: ...

class inputBotInlineMessageGame(TLObject):
    reply_markup: TLObject | None
    def __init__(self, *, reply_markup: TLObject | None = ...) -> None: ...

class inputBotInlineMessageID(TLObject):
    dc_id: int
    id: int
    access_hash: int
    def __init__(self, *, dc_id: int, id: int, access_hash: int) -> None: ...

class inputBotInlineMessageID64(TLObject):
    dc_id: int
    owner_id: int
    id: int
    access_hash: int
    def __init__(self, *, dc_id: int, owner_id: int, id: int, access_hash: int) -> None: ...

class inputBotInlineMessageMediaAuto(TLObject):
    invert_media: bool
    message: str
    entities: list[TLObject] | None
    reply_markup: TLObject | None
    def __init__(self, *, invert_media: bool = ..., message: str, entities: list[TLObject] | None = ..., reply_markup: TLObject | None = ...) -> None: ...

class inputBotInlineMessageMediaContact(TLObject):
    phone_number: str
    first_name: str
    last_name: str
    vcard: str
    reply_markup: TLObject | None
    def __init__(self, *, phone_number: str, first_name: str, last_name: str, vcard: str, reply_markup: TLObject | None = ...) -> None: ...

class inputBotInlineMessageMediaGeo(TLObject):
    geo_point: TLObject
    heading: int | None
    period: int | None
    proximity_notification_radius: int | None
    reply_markup: TLObject | None
    def __init__(self, *, geo_point: TLObject, heading: int | None = ..., period: int | None = ..., proximity_notification_radius: int | None = ..., reply_markup: TLObject | None = ...) -> None: ...

class inputBotInlineMessageMediaInvoice(TLObject):
    title: str
    description: str
    photo: TLObject | None
    invoice: TLObject
    payload: bytes
    provider: str
    provider_data: TLObject
    reply_markup: TLObject | None
    def __init__(self, *, title: str, description: str, photo: TLObject | None = ..., invoice: TLObject, payload: bytes, provider: str, provider_data: TLObject, reply_markup: TLObject | None = ...) -> None: ...

class inputBotInlineMessageMediaVenue(TLObject):
    geo_point: TLObject
    title: str
    address: str
    provider: str
    venue_id: str
    venue_type: str
    reply_markup: TLObject | None
    def __init__(self, *, geo_point: TLObject, title: str, address: str, provider: str, venue_id: str, venue_type: str, reply_markup: TLObject | None = ...) -> None: ...

class inputBotInlineMessageMediaWebPage(TLObject):
    invert_media: bool
    force_large_media: bool
    force_small_media: bool
    optional: bool
    message: str
    entities: list[TLObject] | None
    url: str
    reply_markup: TLObject | None
    def __init__(self, *, invert_media: bool = ..., force_large_media: bool = ..., force_small_media: bool = ..., optional: bool = ..., message: str, entities: list[TLObject] | None = ..., url: str, reply_markup: TLObject | None = ...) -> None: ...

class inputBotInlineMessageRichMessage(TLObject):
    reply_markup: TLObject | None
    rich_message: TLObject
    def __init__(self, *, reply_markup: TLObject | None = ..., rich_message: TLObject) -> None: ...

class inputBotInlineMessageText(TLObject):
    no_webpage: bool
    invert_media: bool
    message: str
    entities: list[TLObject] | None
    reply_markup: TLObject | None
    def __init__(self, *, no_webpage: bool = ..., invert_media: bool = ..., message: str, entities: list[TLObject] | None = ..., reply_markup: TLObject | None = ...) -> None: ...

class inputBotInlineMessageWidget(TLObject):
    allow_queries: bool
    shared_widget: bool
    invert_media: bool
    width: int
    height: int
    html: str
    public_data: str | None
    chat_data: str | None
    reply_markup: TLObject | None
    message: str
    entities: list[TLObject] | None
    def __init__(self, *, allow_queries: bool = ..., shared_widget: bool = ..., invert_media: bool = ..., width: int, height: int, html: str, public_data: str | None = ..., chat_data: str | None = ..., reply_markup: TLObject | None = ..., message: str, entities: list[TLObject] | None = ...) -> None: ...

class inputBotInlineMessageWidgetId(TLObject):
    invert_media: bool
    widget_id: int
    chat_data: str | None
    reply_markup: TLObject | None
    message: str
    entities: list[TLObject] | None
    def __init__(self, *, invert_media: bool = ..., widget_id: int, chat_data: str | None = ..., reply_markup: TLObject | None = ..., message: str, entities: list[TLObject] | None = ...) -> None: ...

class inputBotInlineResult(TLObject):
    id: str
    type: str
    title: str | None
    description: str | None
    url: str | None
    thumb: TLObject | None
    content: TLObject | None
    send_message: TLObject
    def __init__(self, *, id: str, type: str, title: str | None = ..., description: str | None = ..., url: str | None = ..., thumb: TLObject | None = ..., content: TLObject | None = ..., send_message: TLObject) -> None: ...

class inputBotInlineResultDocument(TLObject):
    id: str
    type: str
    title: str | None
    description: str | None
    document: TLObject
    send_message: TLObject
    def __init__(self, *, id: str, type: str, title: str | None = ..., description: str | None = ..., document: TLObject, send_message: TLObject) -> None: ...

class inputBotInlineResultGame(TLObject):
    id: str
    short_name: str
    send_message: TLObject
    def __init__(self, *, id: str, short_name: str, send_message: TLObject) -> None: ...

class inputBotInlineResultPhoto(TLObject):
    id: str
    type: str
    photo: TLObject
    send_message: TLObject
    def __init__(self, *, id: str, type: str, photo: TLObject, send_message: TLObject) -> None: ...

class inputBusinessAwayMessage(TLObject):
    offline_only: bool
    shortcut_id: int
    schedule: TLObject
    recipients: TLObject
    def __init__(self, *, offline_only: bool = ..., shortcut_id: int, schedule: TLObject, recipients: TLObject) -> None: ...

class inputBusinessBotRecipients(TLObject):
    existing_chats: bool
    new_chats: bool
    contacts: bool
    non_contacts: bool
    exclude_selected: bool
    users: list[TLObject] | None
    exclude_users: list[TLObject] | None
    def __init__(self, *, existing_chats: bool = ..., new_chats: bool = ..., contacts: bool = ..., non_contacts: bool = ..., exclude_selected: bool = ..., users: list[TLObject] | None = ..., exclude_users: list[TLObject] | None = ...) -> None: ...

class inputBusinessChatLink(TLObject):
    message: str
    entities: list[TLObject] | None
    title: str | None
    def __init__(self, *, message: str, entities: list[TLObject] | None = ..., title: str | None = ...) -> None: ...

class inputBusinessGreetingMessage(TLObject):
    shortcut_id: int
    recipients: TLObject
    no_activity_days: int
    def __init__(self, *, shortcut_id: int, recipients: TLObject, no_activity_days: int) -> None: ...

class inputBusinessIntro(TLObject):
    title: str
    description: str
    sticker: TLObject | None
    def __init__(self, *, title: str, description: str, sticker: TLObject | None = ...) -> None: ...

class inputBusinessRecipients(TLObject):
    existing_chats: bool
    new_chats: bool
    contacts: bool
    non_contacts: bool
    exclude_selected: bool
    users: list[TLObject] | None
    def __init__(self, *, existing_chats: bool = ..., new_chats: bool = ..., contacts: bool = ..., non_contacts: bool = ..., exclude_selected: bool = ..., users: list[TLObject] | None = ...) -> None: ...

class inputButtonTypeRequestPeer(TLObject):
    name_requested: bool
    username_requested: bool
    photo_requested: bool
    button_id: int
    peer_type: TLObject
    max_quantity: int
    def __init__(self, *, name_requested: bool = ..., username_requested: bool = ..., photo_requested: bool = ..., button_id: int, peer_type: TLObject, max_quantity: int) -> None: ...

class inputChannel(TLObject):
    channel_id: int
    access_hash: int
    def __init__(self, *, channel_id: int, access_hash: int) -> None: ...

class inputChannelEmpty(TLObject):
    def __init__(self) -> None: ...

class inputChannelFromMessage(TLObject):
    peer: TLObject
    msg_id: int
    channel_id: int
    def __init__(self, *, peer: TLObject, msg_id: int, channel_id: int) -> None: ...

class inputChatPhoto(TLObject):
    id: TLObject
    def __init__(self, *, id: TLObject) -> None: ...

class inputChatPhotoEmpty(TLObject):
    def __init__(self) -> None: ...

class inputChatTheme(TLObject):
    emoticon: str
    def __init__(self, *, emoticon: str) -> None: ...

class inputChatThemeEmpty(TLObject):
    def __init__(self) -> None: ...

class inputChatThemeUniqueGift(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class inputChatUploadedPhoto(TLObject):
    file: TLObject | None
    video: TLObject | None
    video_start_ts: float | None
    video_emoji_markup: TLObject | None
    def __init__(self, *, file: TLObject | None = ..., video: TLObject | None = ..., video_start_ts: float | None = ..., video_emoji_markup: TLObject | None = ...) -> None: ...

class inputChatlistDialogFilter(TLObject):
    filter_id: int
    def __init__(self, *, filter_id: int) -> None: ...

class inputCheckPasswordEmpty(TLObject):
    def __init__(self) -> None: ...

class inputCheckPasswordSRP(TLObject):
    srp_id: int
    A: bytes
    M1: bytes
    def __init__(self, *, srp_id: int, A: bytes, M1: bytes) -> None: ...

class inputClientProxy(TLObject):
    address: str
    port: int
    def __init__(self, *, address: str, port: int) -> None: ...

class inputCollectiblePhone(TLObject):
    phone: str
    def __init__(self, *, phone: str) -> None: ...

class inputCollectibleUsername(TLObject):
    username: str
    def __init__(self, *, username: str) -> None: ...

class inputDialogPeer(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class inputDialogPeerCommunity(TLObject):
    community: TLObject
    def __init__(self, *, community: TLObject) -> None: ...

class inputDialogPeerFolder(TLObject):
    folder_id: int
    def __init__(self, *, folder_id: int) -> None: ...

class inputDocument(TLObject):
    id: int
    access_hash: int
    file_reference: bytes
    def __init__(self, *, id: int, access_hash: int, file_reference: bytes) -> None: ...

class inputDocumentEmpty(TLObject):
    def __init__(self) -> None: ...

class inputDocumentFileLocation(TLObject):
    id: int
    access_hash: int
    file_reference: bytes
    thumb_size: str
    def __init__(self, *, id: int, access_hash: int, file_reference: bytes, thumb_size: str) -> None: ...

class inputEmojiStatusCollectible(TLObject):
    collectible_id: int
    until: int | None
    def __init__(self, *, collectible_id: int, until: int | None = ...) -> None: ...

class inputEncryptedChat(TLObject):
    chat_id: int
    access_hash: int
    def __init__(self, *, chat_id: int, access_hash: int) -> None: ...

class inputEncryptedFile(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputEncryptedFileBigUploaded(TLObject):
    id: int
    parts: int
    key_fingerprint: int
    def __init__(self, *, id: int, parts: int, key_fingerprint: int) -> None: ...

class inputEncryptedFileEmpty(TLObject):
    def __init__(self) -> None: ...

class inputEncryptedFileLocation(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputEncryptedFileUploaded(TLObject):
    id: int
    parts: int
    md5_checksum: str
    key_fingerprint: int
    def __init__(self, *, id: int, parts: int, md5_checksum: str, key_fingerprint: int) -> None: ...

class inputFile(TLObject):
    id: int
    parts: int
    name: str
    md5_checksum: str
    def __init__(self, *, id: int, parts: int, name: str, md5_checksum: str) -> None: ...

class inputFileBig(TLObject):
    id: int
    parts: int
    name: str
    def __init__(self, *, id: int, parts: int, name: str) -> None: ...

class inputFileLocation(TLObject):
    volume_id: int
    local_id: int
    secret: int
    file_reference: bytes
    def __init__(self, *, volume_id: int, local_id: int, secret: int, file_reference: bytes) -> None: ...

class inputFileStoryDocument(TLObject):
    id: TLObject
    def __init__(self, *, id: TLObject) -> None: ...

class inputFolderPeer(TLObject):
    peer: TLObject
    folder_id: int
    def __init__(self, *, peer: TLObject, folder_id: int) -> None: ...

class inputGameID(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputGameShortName(TLObject):
    bot_id: TLObject
    short_name: str
    def __init__(self, *, bot_id: TLObject, short_name: str) -> None: ...

class inputGeoPoint(TLObject):
    lat: float
    long: float
    accuracy_radius: int | None
    def __init__(self, *, lat: float, long: float, accuracy_radius: int | None = ...) -> None: ...

class inputGeoPointEmpty(TLObject):
    def __init__(self) -> None: ...

class inputGroupCall(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputGroupCallInviteMessage(TLObject):
    msg_id: int
    def __init__(self, *, msg_id: int) -> None: ...

class inputGroupCallSlug(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class inputGroupCallStream(TLObject):
    call: TLObject
    time_ms: int
    scale: int
    video_channel: int | None
    video_quality: int | None
    def __init__(self, *, call: TLObject, time_ms: int, scale: int, video_channel: int | None = ..., video_quality: int | None = ...) -> None: ...

class inputInlineButtonTypeUrlAuth(TLObject):
    request_write_access: bool
    fwd_text: str | None
    url: str
    bot: TLObject | None
    def __init__(self, *, request_write_access: bool = ..., fwd_text: str | None = ..., url: str, bot: TLObject | None = ...) -> None: ...

class inputInlineButtonTypeUserProfile(TLObject):
    user_id: TLObject
    def __init__(self, *, user_id: TLObject) -> None: ...

class inputInvoiceBusinessBotTransferStars(TLObject):
    bot: TLObject
    stars: int
    def __init__(self, *, bot: TLObject, stars: int) -> None: ...

class inputInvoiceChatInviteSubscription(TLObject):
    hash: str
    def __init__(self, *, hash: str) -> None: ...

class inputInvoiceMessage(TLObject):
    peer: TLObject
    msg_id: int
    def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

class inputInvoicePremiumAuthCode(TLObject):
    purpose: TLObject
    def __init__(self, *, purpose: TLObject) -> None: ...

class inputInvoicePremiumGiftCode(TLObject):
    purpose: TLObject
    option: TLObject
    def __init__(self, *, purpose: TLObject, option: TLObject) -> None: ...

class inputInvoicePremiumGiftStars(TLObject):
    user_id: TLObject
    months: int
    message: TLObject | None
    def __init__(self, *, user_id: TLObject, months: int, message: TLObject | None = ...) -> None: ...

class inputInvoiceSlug(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class inputInvoiceStarGift(TLObject):
    hide_name: bool
    include_upgrade: bool
    peer: TLObject
    gift_id: int
    message: TLObject | None
    def __init__(self, *, hide_name: bool = ..., include_upgrade: bool = ..., peer: TLObject, gift_id: int, message: TLObject | None = ...) -> None: ...

class inputInvoiceStarGiftAuctionBid(TLObject):
    hide_name: bool
    update_bid: bool
    peer: TLObject | None
    gift_id: int
    bid_amount: int
    message: TLObject | None
    def __init__(self, *, hide_name: bool = ..., update_bid: bool = ..., peer: TLObject | None = ..., gift_id: int, bid_amount: int, message: TLObject | None = ...) -> None: ...

class inputInvoiceStarGiftDropOriginalDetails(TLObject):
    stargift: TLObject
    def __init__(self, *, stargift: TLObject) -> None: ...

class inputInvoiceStarGiftPrepaidUpgrade(TLObject):
    peer: TLObject
    hash: str
    def __init__(self, *, peer: TLObject, hash: str) -> None: ...

class inputInvoiceStarGiftResale(TLObject):
    ton: bool
    show_name: bool
    slug: str
    to_id: TLObject
    message: TLObject | None
    def __init__(self, *, ton: bool = ..., show_name: bool = ..., slug: str, to_id: TLObject, message: TLObject | None = ...) -> None: ...

class inputInvoiceStarGiftTransfer(TLObject):
    stargift: TLObject
    to_id: TLObject
    def __init__(self, *, stargift: TLObject, to_id: TLObject) -> None: ...

class inputInvoiceStarGiftUpgrade(TLObject):
    keep_original_details: bool
    stargift: TLObject
    def __init__(self, *, keep_original_details: bool = ..., stargift: TLObject) -> None: ...

class inputInvoiceStars(TLObject):
    purpose: TLObject
    def __init__(self, *, purpose: TLObject) -> None: ...

class inputMediaAreaChannelPost(TLObject):
    coordinates: TLObject
    channel: TLObject
    msg_id: int
    def __init__(self, *, coordinates: TLObject, channel: TLObject, msg_id: int) -> None: ...

class inputMediaAreaVenue(TLObject):
    coordinates: TLObject
    query_id: int
    result_id: str
    def __init__(self, *, coordinates: TLObject, query_id: int, result_id: str) -> None: ...

class inputMediaContact(TLObject):
    phone_number: str
    first_name: str
    last_name: str
    vcard: str
    def __init__(self, *, phone_number: str, first_name: str, last_name: str, vcard: str) -> None: ...

class inputMediaDice(TLObject):
    emoticon: str
    def __init__(self, *, emoticon: str) -> None: ...

class inputMediaDocument(TLObject):
    spoiler: bool
    id: TLObject
    video_cover: TLObject | None
    video_timestamp: int | None
    ttl_seconds: int | None
    query: str | None
    def __init__(self, *, spoiler: bool = ..., id: TLObject, video_cover: TLObject | None = ..., video_timestamp: int | None = ..., ttl_seconds: int | None = ..., query: str | None = ...) -> None: ...

class inputMediaDocumentExternal(TLObject):
    spoiler: bool
    url: str
    ttl_seconds: int | None
    video_cover: TLObject | None
    video_timestamp: int | None
    def __init__(self, *, spoiler: bool = ..., url: str, ttl_seconds: int | None = ..., video_cover: TLObject | None = ..., video_timestamp: int | None = ...) -> None: ...

class inputMediaEmpty(TLObject):
    def __init__(self) -> None: ...

class inputMediaGame(TLObject):
    id: TLObject
    def __init__(self, *, id: TLObject) -> None: ...

class inputMediaGeoLive(TLObject):
    stopped: bool
    geo_point: TLObject
    heading: int | None
    period: int | None
    proximity_notification_radius: int | None
    def __init__(self, *, stopped: bool = ..., geo_point: TLObject, heading: int | None = ..., period: int | None = ..., proximity_notification_radius: int | None = ...) -> None: ...

class inputMediaGeoPoint(TLObject):
    geo_point: TLObject
    def __init__(self, *, geo_point: TLObject) -> None: ...

class inputMediaInvoice(TLObject):
    title: str
    description: str
    photo: TLObject | None
    invoice: TLObject
    payload: bytes
    provider: str | None
    provider_data: TLObject
    start_param: str | None
    extended_media: TLObject | None
    def __init__(self, *, title: str, description: str, photo: TLObject | None = ..., invoice: TLObject, payload: bytes, provider: str | None = ..., provider_data: TLObject, start_param: str | None = ..., extended_media: TLObject | None = ...) -> None: ...

class inputMediaPaidMedia(TLObject):
    stars_amount: int
    extended_media: list[TLObject]
    payload: str | None
    def __init__(self, *, stars_amount: int, extended_media: list[TLObject], payload: str | None = ...) -> None: ...

class inputMediaPhoto(TLObject):
    spoiler: bool
    live_photo: bool
    id: TLObject
    ttl_seconds: int | None
    video: TLObject | None
    def __init__(self, *, spoiler: bool = ..., live_photo: bool = ..., id: TLObject, ttl_seconds: int | None = ..., video: TLObject | None = ...) -> None: ...

class inputMediaPhotoExternal(TLObject):
    spoiler: bool
    url: str
    ttl_seconds: int | None
    def __init__(self, *, spoiler: bool = ..., url: str, ttl_seconds: int | None = ...) -> None: ...

class inputMediaPoll(TLObject):
    poll: TLObject
    correct_answers: list[int] | None
    attached_media: TLObject | None
    solution: str | None
    solution_entities: list[TLObject] | None
    solution_media: TLObject | None
    def __init__(self, *, poll: TLObject, correct_answers: list[int] | None = ..., attached_media: TLObject | None = ..., solution: str | None = ..., solution_entities: list[TLObject] | None = ..., solution_media: TLObject | None = ...) -> None: ...

class inputMediaStakeDice(TLObject):
    game_hash: str
    ton_amount: int
    client_seed: bytes
    def __init__(self, *, game_hash: str, ton_amount: int, client_seed: bytes) -> None: ...

class inputMediaStory(TLObject):
    peer: TLObject
    id: int
    def __init__(self, *, peer: TLObject, id: int) -> None: ...

class inputMediaTodo(TLObject):
    todo: TLObject
    def __init__(self, *, todo: TLObject) -> None: ...

class inputMediaUploadedDocument(TLObject):
    nosound_video: bool
    force_file: bool
    spoiler: bool
    file: TLObject
    thumb: TLObject | None
    mime_type: str
    attributes: list[TLObject]
    stickers: list[TLObject] | None
    video_cover: TLObject | None
    video_timestamp: int | None
    ttl_seconds: int | None
    def __init__(self, *, nosound_video: bool = ..., force_file: bool = ..., spoiler: bool = ..., file: TLObject, thumb: TLObject | None = ..., mime_type: str, attributes: list[TLObject], stickers: list[TLObject] | None = ..., video_cover: TLObject | None = ..., video_timestamp: int | None = ..., ttl_seconds: int | None = ...) -> None: ...

class inputMediaUploadedPhoto(TLObject):
    spoiler: bool
    live_photo: bool
    file: TLObject
    stickers: list[TLObject] | None
    ttl_seconds: int | None
    video: TLObject | None
    def __init__(self, *, spoiler: bool = ..., live_photo: bool = ..., file: TLObject, stickers: list[TLObject] | None = ..., ttl_seconds: int | None = ..., video: TLObject | None = ...) -> None: ...

class inputMediaVenue(TLObject):
    geo_point: TLObject
    title: str
    address: str
    provider: str
    venue_id: str
    venue_type: str
    def __init__(self, *, geo_point: TLObject, title: str, address: str, provider: str, venue_id: str, venue_type: str) -> None: ...

class inputMediaWebPage(TLObject):
    force_large_media: bool
    force_small_media: bool
    optional: bool
    url: str
    def __init__(self, *, force_large_media: bool = ..., force_small_media: bool = ..., optional: bool = ..., url: str) -> None: ...

class inputMediaWidget(TLObject):
    allow_queries: bool
    shared_widget: bool
    width: int
    height: int
    html: str
    public_data: str | None
    chat_data: str | None
    def __init__(self, *, allow_queries: bool = ..., shared_widget: bool = ..., width: int, height: int, html: str, public_data: str | None = ..., chat_data: str | None = ...) -> None: ...

class inputMediaWidgetId(TLObject):
    widget_id: int
    chat_data: str | None
    def __init__(self, *, widget_id: int, chat_data: str | None = ...) -> None: ...

class inputMessageCallbackQuery(TLObject):
    id: int
    query_id: int
    def __init__(self, *, id: int, query_id: int) -> None: ...

class inputMessageEntityMentionName(TLObject):
    offset: int
    length: int
    user_id: TLObject
    def __init__(self, *, offset: int, length: int, user_id: TLObject) -> None: ...

class inputMessageID(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class inputMessagePinned(TLObject):
    def __init__(self) -> None: ...

class inputMessageReadMetric(TLObject):
    msg_id: int
    view_id: int
    time_in_view_ms: int
    active_time_in_view_ms: int
    height_to_viewport_ratio_permille: int
    seen_range_ratio_permille: int
    def __init__(self, *, msg_id: int, view_id: int, time_in_view_ms: int, active_time_in_view_ms: int, height_to_viewport_ratio_permille: int, seen_range_ratio_permille: int) -> None: ...

class inputMessageReplyTo(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class inputMessagesFilterChatPhotos(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterContacts(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterDocument(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterEmpty(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterGeo(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterGif(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterMusic(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterMyMentions(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterPhoneCalls(TLObject):
    missed: bool
    def __init__(self, *, missed: bool = ...) -> None: ...

class inputMessagesFilterPhotoVideo(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterPhotos(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterPinned(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterPoll(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterRoundVideo(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterRoundVoice(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterUrl(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterVideo(TLObject):
    def __init__(self) -> None: ...

class inputMessagesFilterVoice(TLObject):
    def __init__(self) -> None: ...

class inputNotifyBroadcasts(TLObject):
    def __init__(self) -> None: ...

class inputNotifyChats(TLObject):
    def __init__(self) -> None: ...

class inputNotifyCommunity(TLObject):
    community: TLObject
    def __init__(self, *, community: TLObject) -> None: ...

class inputNotifyForumTopic(TLObject):
    peer: TLObject
    top_msg_id: int
    def __init__(self, *, peer: TLObject, top_msg_id: int) -> None: ...

class inputNotifyPeer(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class inputNotifyUsers(TLObject):
    def __init__(self) -> None: ...

class inputPageBlockMap(TLObject):
    geo: TLObject
    zoom: int
    w: int
    h: int
    caption: TLObject
    def __init__(self, *, geo: TLObject, zoom: int, w: int, h: int, caption: TLObject) -> None: ...

class inputPasskeyCredentialPublicKey(TLObject):
    id: str
    raw_id: str
    response: TLObject
    def __init__(self, *, id: str, raw_id: str, response: TLObject) -> None: ...

class inputPasskeyResponseLogin(TLObject):
    client_data: TLObject
    authenticator_data: bytes
    signature: bytes
    user_handle: str
    def __init__(self, *, client_data: TLObject, authenticator_data: bytes, signature: bytes, user_handle: str) -> None: ...

class inputPasskeyResponseRegister(TLObject):
    client_data: TLObject
    attestation_data: bytes
    def __init__(self, *, client_data: TLObject, attestation_data: bytes) -> None: ...

class inputPaymentCredentials(TLObject):
    save: bool
    data: TLObject
    def __init__(self, *, save: bool = ..., data: TLObject) -> None: ...

class inputPaymentCredentialsApplePay(TLObject):
    payment_data: TLObject
    def __init__(self, *, payment_data: TLObject) -> None: ...

class inputPaymentCredentialsGooglePay(TLObject):
    payment_token: TLObject
    def __init__(self, *, payment_token: TLObject) -> None: ...

class inputPaymentCredentialsSaved(TLObject):
    id: str
    tmp_password: bytes
    def __init__(self, *, id: str, tmp_password: bytes) -> None: ...

class inputPeerChannel(TLObject):
    channel_id: int
    access_hash: int
    def __init__(self, *, channel_id: int, access_hash: int) -> None: ...

class inputPeerChannelFromMessage(TLObject):
    peer: TLObject
    msg_id: int
    channel_id: int
    def __init__(self, *, peer: TLObject, msg_id: int, channel_id: int) -> None: ...

class inputPeerChat(TLObject):
    chat_id: int
    def __init__(self, *, chat_id: int) -> None: ...

class inputPeerColorCollectible(TLObject):
    collectible_id: int
    def __init__(self, *, collectible_id: int) -> None: ...

class inputPeerEmpty(TLObject):
    def __init__(self) -> None: ...

class inputPeerNotifySettings(TLObject):
    show_previews: bool
    silent: bool
    mute_until: int | None
    sound: TLObject | None
    stories_muted: bool
    stories_hide_sender: bool
    stories_sound: TLObject | None
    def __init__(self, *, show_previews: bool = ..., silent: bool = ..., mute_until: int | None = ..., sound: TLObject | None = ..., stories_muted: bool = ..., stories_hide_sender: bool = ..., stories_sound: TLObject | None = ...) -> None: ...

class inputPeerPhotoFileLocation(TLObject):
    big: bool
    peer: TLObject
    photo_id: int
    def __init__(self, *, big: bool = ..., peer: TLObject, photo_id: int) -> None: ...

class inputPeerSelf(TLObject):
    def __init__(self) -> None: ...

class inputPeerUser(TLObject):
    user_id: int
    access_hash: int
    def __init__(self, *, user_id: int, access_hash: int) -> None: ...

class inputPeerUserFromMessage(TLObject):
    peer: TLObject
    msg_id: int
    user_id: int
    def __init__(self, *, peer: TLObject, msg_id: int, user_id: int) -> None: ...

class inputPhoneCall(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputPhoneContact(TLObject):
    client_id: int
    phone: str
    first_name: str
    last_name: str
    note: TLObject | None
    def __init__(self, *, client_id: int, phone: str, first_name: str, last_name: str, note: TLObject | None = ...) -> None: ...

class inputPhoto(TLObject):
    id: int
    access_hash: int
    file_reference: bytes
    def __init__(self, *, id: int, access_hash: int, file_reference: bytes) -> None: ...

class inputPhotoEmpty(TLObject):
    def __init__(self) -> None: ...

class inputPhotoFileLocation(TLObject):
    id: int
    access_hash: int
    file_reference: bytes
    thumb_size: str
    def __init__(self, *, id: int, access_hash: int, file_reference: bytes, thumb_size: str) -> None: ...

class inputPhotoLegacyFileLocation(TLObject):
    id: int
    access_hash: int
    file_reference: bytes
    volume_id: int
    local_id: int
    secret: int
    def __init__(self, *, id: int, access_hash: int, file_reference: bytes, volume_id: int, local_id: int, secret: int) -> None: ...

class inputPollAnswer(TLObject):
    text: TLObject
    media: TLObject | None
    def __init__(self, *, text: TLObject, media: TLObject | None = ...) -> None: ...

class inputPrivacyKeyAbout(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyAddedByPhone(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyBirthday(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyChatInvite(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyForwards(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyNoPaidMessages(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyPhoneCall(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyPhoneNumber(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyPhoneP2P(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyProfilePhoto(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeySavedMusic(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyStarGiftsAutoSave(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyStatusTimestamp(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyKeyVoiceMessages(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueAllowAll(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueAllowBots(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueAllowChatParticipants(TLObject):
    chats: list[int]
    def __init__(self, *, chats: list[int]) -> None: ...

class inputPrivacyValueAllowCloseFriends(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueAllowContacts(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueAllowPremium(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueAllowUsers(TLObject):
    users: list[TLObject]
    def __init__(self, *, users: list[TLObject]) -> None: ...

class inputPrivacyValueDisallowAll(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueDisallowBots(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueDisallowChatParticipants(TLObject):
    chats: list[int]
    def __init__(self, *, chats: list[int]) -> None: ...

class inputPrivacyValueDisallowContacts(TLObject):
    def __init__(self) -> None: ...

class inputPrivacyValueDisallowUsers(TLObject):
    users: list[TLObject]
    def __init__(self, *, users: list[TLObject]) -> None: ...

class inputQuickReplyShortcut(TLObject):
    shortcut: str
    def __init__(self, *, shortcut: str) -> None: ...

class inputQuickReplyShortcutId(TLObject):
    shortcut_id: int
    def __init__(self, *, shortcut_id: int) -> None: ...

class inputReplyToEphemeralMessage(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class inputReplyToMessage(TLObject):
    reply_to_msg_id: int
    top_msg_id: int | None
    reply_to_peer_id: TLObject | None
    quote_text: str | None
    quote_entities: list[TLObject] | None
    quote_offset: int | None
    monoforum_peer_id: TLObject | None
    todo_item_id: int | None
    poll_option: bytes | None
    quote_rich: list[TLObject] | None
    def __init__(self, *, reply_to_msg_id: int, top_msg_id: int | None = ..., reply_to_peer_id: TLObject | None = ..., quote_text: str | None = ..., quote_entities: list[TLObject] | None = ..., quote_offset: int | None = ..., monoforum_peer_id: TLObject | None = ..., todo_item_id: int | None = ..., poll_option: bytes | None = ..., quote_rich: list[TLObject] | None = ...) -> None: ...

class inputReplyToMonoForum(TLObject):
    monoforum_peer_id: TLObject
    def __init__(self, *, monoforum_peer_id: TLObject) -> None: ...

class inputReplyToStory(TLObject):
    peer: TLObject
    story_id: int
    def __init__(self, *, peer: TLObject, story_id: int) -> None: ...

class inputReportReasonChildAbuse(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonCopyright(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonFake(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonGeoIrrelevant(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonIllegalDrugs(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonOther(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonPersonalDetails(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonPornography(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonSpam(TLObject):
    def __init__(self) -> None: ...

class inputReportReasonViolence(TLObject):
    def __init__(self) -> None: ...

class inputRichFileDocument(TLObject):
    id: str
    document: TLObject
    def __init__(self, *, id: str, document: TLObject) -> None: ...

class inputRichFilePhoto(TLObject):
    id: str
    photo: TLObject
    def __init__(self, *, id: str, photo: TLObject) -> None: ...

class inputRichMessage(TLObject):
    rtl: bool
    noautolink: bool
    blocks: list[TLObject]
    photos: list[TLObject] | None
    documents: list[TLObject] | None
    users: list[TLObject] | None
    def __init__(self, *, rtl: bool = ..., noautolink: bool = ..., blocks: list[TLObject], photos: list[TLObject] | None = ..., documents: list[TLObject] | None = ..., users: list[TLObject] | None = ...) -> None: ...

class inputRichMessageHTML(TLObject):
    rtl: bool
    noautolink: bool
    html: str
    files: list[TLObject] | None
    def __init__(self, *, rtl: bool = ..., noautolink: bool = ..., html: str, files: list[TLObject] | None = ...) -> None: ...

class inputRichMessageMarkdown(TLObject):
    rtl: bool
    noautolink: bool
    markdown: str
    files: list[TLObject] | None
    def __init__(self, *, rtl: bool = ..., noautolink: bool = ..., markdown: str, files: list[TLObject] | None = ...) -> None: ...

class inputSavedStarGiftChat(TLObject):
    peer: TLObject
    saved_id: int
    def __init__(self, *, peer: TLObject, saved_id: int) -> None: ...

class inputSavedStarGiftSlug(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class inputSavedStarGiftUser(TLObject):
    msg_id: int
    def __init__(self, *, msg_id: int) -> None: ...

class inputSecureFile(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputSecureFileLocation(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputSecureFileUploaded(TLObject):
    id: int
    parts: int
    md5_checksum: str
    file_hash: bytes
    secret: bytes
    def __init__(self, *, id: int, parts: int, md5_checksum: str, file_hash: bytes, secret: bytes) -> None: ...

class inputSecureValue(TLObject):
    type: TLObject
    data: TLObject | None
    front_side: TLObject | None
    reverse_side: TLObject | None
    selfie: TLObject | None
    translation: list[TLObject] | None
    files: list[TLObject] | None
    plain_data: TLObject | None
    def __init__(self, *, type: TLObject, data: TLObject | None = ..., front_side: TLObject | None = ..., reverse_side: TLObject | None = ..., selfie: TLObject | None = ..., translation: list[TLObject] | None = ..., files: list[TLObject] | None = ..., plain_data: TLObject | None = ...) -> None: ...

class inputSendMessageRichMessageDraftAction(TLObject):
    can_stop: bool
    keep_on_stop: bool
    random_id: int
    rich_message: TLObject
    def __init__(self, *, can_stop: bool = ..., keep_on_stop: bool = ..., random_id: int, rich_message: TLObject) -> None: ...

class inputShareThemeGift(TLObject):
    stargift: TLObject
    def __init__(self, *, stargift: TLObject) -> None: ...

class inputSingleMedia(TLObject):
    media: TLObject
    random_id: int
    message: str
    entities: list[TLObject] | None
    def __init__(self, *, media: TLObject, random_id: int, message: str, entities: list[TLObject] | None = ...) -> None: ...

class inputStarGiftAuction(TLObject):
    gift_id: int
    def __init__(self, *, gift_id: int) -> None: ...

class inputStarGiftAuctionSlug(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class inputStarsTransaction(TLObject):
    refund: bool
    id: str
    def __init__(self, *, refund: bool = ..., id: str) -> None: ...

class inputStickerSetAnimatedEmoji(TLObject):
    def __init__(self) -> None: ...

class inputStickerSetAnimatedEmojiAnimations(TLObject):
    def __init__(self) -> None: ...

class inputStickerSetDice(TLObject):
    emoticon: str
    def __init__(self, *, emoticon: str) -> None: ...

class inputStickerSetEmojiChannelDefaultStatuses(TLObject):
    def __init__(self) -> None: ...

class inputStickerSetEmojiDefaultStatuses(TLObject):
    def __init__(self) -> None: ...

class inputStickerSetEmojiDefaultTopicIcons(TLObject):
    def __init__(self) -> None: ...

class inputStickerSetEmojiGenericAnimations(TLObject):
    def __init__(self) -> None: ...

class inputStickerSetEmpty(TLObject):
    def __init__(self) -> None: ...

class inputStickerSetID(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputStickerSetItem(TLObject):
    document: TLObject
    emoji: str
    mask_coords: TLObject | None
    keywords: str | None
    def __init__(self, *, document: TLObject, emoji: str, mask_coords: TLObject | None = ..., keywords: str | None = ...) -> None: ...

class inputStickerSetPremiumGifts(TLObject):
    def __init__(self) -> None: ...

class inputStickerSetShortName(TLObject):
    short_name: str
    def __init__(self, *, short_name: str) -> None: ...

class inputStickerSetThumb(TLObject):
    stickerset: TLObject
    thumb_version: int
    def __init__(self, *, stickerset: TLObject, thumb_version: int) -> None: ...

class inputStickerSetTonGifts(TLObject):
    def __init__(self) -> None: ...

class inputStickeredMediaDocument(TLObject):
    id: TLObject
    def __init__(self, *, id: TLObject) -> None: ...

class inputStickeredMediaPhoto(TLObject):
    id: TLObject
    def __init__(self, *, id: TLObject) -> None: ...

class inputStorePaymentAuthCode(TLObject):
    restore: bool
    phone_number: str
    phone_code_hash: str
    premium_days: int
    currency: str
    amount: int
    def __init__(self, *, restore: bool = ..., phone_number: str, phone_code_hash: str, premium_days: int, currency: str, amount: int) -> None: ...

class inputStorePaymentGiftPremium(TLObject):
    user_id: TLObject
    currency: str
    amount: int
    def __init__(self, *, user_id: TLObject, currency: str, amount: int) -> None: ...

class inputStorePaymentPremiumGiftCode(TLObject):
    users: list[TLObject]
    boost_peer: TLObject | None
    currency: str
    amount: int
    message: TLObject | None
    def __init__(self, *, users: list[TLObject], boost_peer: TLObject | None = ..., currency: str, amount: int, message: TLObject | None = ...) -> None: ...

class inputStorePaymentPremiumGiveaway(TLObject):
    only_new_subscribers: bool
    winners_are_visible: bool
    boost_peer: TLObject
    additional_peers: list[TLObject] | None
    countries_iso2: list[str] | None
    prize_description: str | None
    random_id: int
    until_date: int
    currency: str
    amount: int
    def __init__(self, *, only_new_subscribers: bool = ..., winners_are_visible: bool = ..., boost_peer: TLObject, additional_peers: list[TLObject] | None = ..., countries_iso2: list[str] | None = ..., prize_description: str | None = ..., random_id: int, until_date: int, currency: str, amount: int) -> None: ...

class inputStorePaymentPremiumSubscription(TLObject):
    restore: bool
    upgrade: bool
    def __init__(self, *, restore: bool = ..., upgrade: bool = ...) -> None: ...

class inputStorePaymentStarsGift(TLObject):
    user_id: TLObject
    stars: int
    currency: str
    amount: int
    def __init__(self, *, user_id: TLObject, stars: int, currency: str, amount: int) -> None: ...

class inputStorePaymentStarsGiveaway(TLObject):
    only_new_subscribers: bool
    winners_are_visible: bool
    stars: int
    boost_peer: TLObject
    additional_peers: list[TLObject] | None
    countries_iso2: list[str] | None
    prize_description: str | None
    random_id: int
    until_date: int
    currency: str
    amount: int
    users: int
    def __init__(self, *, only_new_subscribers: bool = ..., winners_are_visible: bool = ..., stars: int, boost_peer: TLObject, additional_peers: list[TLObject] | None = ..., countries_iso2: list[str] | None = ..., prize_description: str | None = ..., random_id: int, until_date: int, currency: str, amount: int, users: int) -> None: ...

class inputStorePaymentStarsTopup(TLObject):
    stars: int
    currency: str
    amount: int
    spend_purpose_peer: TLObject | None
    def __init__(self, *, stars: int, currency: str, amount: int, spend_purpose_peer: TLObject | None = ...) -> None: ...

class inputTakeoutFileLocation(TLObject):
    def __init__(self) -> None: ...

class inputTheme(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputThemeSettings(TLObject):
    message_colors_animated: bool
    base_theme: TLObject
    accent_color: int
    outbox_accent_color: int | None
    message_colors: list[int] | None
    wallpaper: TLObject | None
    wallpaper_settings: TLObject | None
    def __init__(self, *, message_colors_animated: bool = ..., base_theme: TLObject, accent_color: int, outbox_accent_color: int | None = ..., message_colors: list[int] | None = ..., wallpaper: TLObject | None = ..., wallpaper_settings: TLObject | None = ...) -> None: ...

class inputThemeSlug(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class inputTonConnectOauthSession(TLObject):
    session_id: int
    challenge_answer: bytes
    body: bytes
    proof: TLObject
    def __init__(self, *, session_id: int, challenge_answer: bytes, body: bytes, proof: TLObject) -> None: ...

class inputUser(TLObject):
    user_id: int
    access_hash: int
    def __init__(self, *, user_id: int, access_hash: int) -> None: ...

class inputUserEmpty(TLObject):
    def __init__(self) -> None: ...

class inputUserFromMessage(TLObject):
    peer: TLObject
    msg_id: int
    user_id: int
    def __init__(self, *, peer: TLObject, msg_id: int, user_id: int) -> None: ...

class inputUserSelf(TLObject):
    def __init__(self) -> None: ...

class inputWallPaper(TLObject):
    id: int
    access_hash: int
    def __init__(self, *, id: int, access_hash: int) -> None: ...

class inputWallPaperNoFile(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class inputWallPaperSlug(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class inputWalletCardSticker(TLObject):
    coordinates: TLObject
    nft_address: str
    def __init__(self, *, coordinates: TLObject, nft_address: str) -> None: ...

class inputWalletImported(TLObject):
    public_key: bytes
    anchor_public_key: bytes | None
    proof: TLObject
    def __init__(self, *, public_key: bytes, anchor_public_key: bytes | None = ..., proof: TLObject) -> None: ...

class inputWalletNew(TLObject):
    def __init__(self) -> None: ...

class inputWebDocument(TLObject):
    url: str
    size: int
    mime_type: str
    attributes: list[TLObject]
    def __init__(self, *, url: str, size: int, mime_type: str, attributes: list[TLObject]) -> None: ...

class inputWebFileAudioAlbumThumbLocation(TLObject):
    small: bool
    document: TLObject | None
    title: str | None
    performer: str | None
    def __init__(self, *, small: bool = ..., document: TLObject | None = ..., title: str | None = ..., performer: str | None = ...) -> None: ...

class inputWebFileGeoPointLocation(TLObject):
    geo_point: TLObject
    access_hash: int
    w: int
    h: int
    zoom: int
    scale: int
    def __init__(self, *, geo_point: TLObject, access_hash: int, w: int, h: int, zoom: int, scale: int) -> None: ...

class inputWebFileLocation(TLObject):
    url: str
    access_hash: int
    def __init__(self, *, url: str, access_hash: int) -> None: ...

class invoice(TLObject):
    test: bool
    name_requested: bool
    phone_requested: bool
    email_requested: bool
    shipping_address_requested: bool
    flexible: bool
    phone_to_provider: bool
    email_to_provider: bool
    recurring: bool
    currency: str
    prices: list[TLObject]
    max_tip_amount: int | None
    suggested_tip_amounts: list[int] | None
    terms_url: str | None
    subscription_period: int | None
    def __init__(self, *, test: bool = ..., name_requested: bool = ..., phone_requested: bool = ..., email_requested: bool = ..., shipping_address_requested: bool = ..., flexible: bool = ..., phone_to_provider: bool = ..., email_to_provider: bool = ..., recurring: bool = ..., currency: str, prices: list[TLObject], max_tip_amount: int | None = ..., suggested_tip_amounts: list[int] | None = ..., terms_url: str | None = ..., subscription_period: int | None = ...) -> None: ...

class invokeAfterMsg(TLObject):
    msg_id: int
    query: TLObject
    def __init__(self, *, msg_id: int, query: TLObject) -> None: ...

class invokeAfterMsgs(TLObject):
    msg_ids: list[int]
    query: TLObject
    def __init__(self, *, msg_ids: list[int], query: TLObject) -> None: ...

class invokeWithApnsSecret(TLObject):
    nonce: str
    secret: str
    query: TLObject
    def __init__(self, *, nonce: str, secret: str, query: TLObject) -> None: ...

class invokeWithBusinessConnection(TLObject):
    connection_id: str
    query: TLObject
    def __init__(self, *, connection_id: str, query: TLObject) -> None: ...

class invokeWithGooglePlayIntegrity(TLObject):
    nonce: str
    token: str
    query: TLObject
    def __init__(self, *, nonce: str, token: str, query: TLObject) -> None: ...

class invokeWithLayer(TLObject):
    layer: int
    query: TLObject
    def __init__(self, *, layer: int, query: TLObject) -> None: ...

class invokeWithMessagesRange(TLObject):
    range: TLObject
    query: TLObject
    def __init__(self, *, range: TLObject, query: TLObject) -> None: ...

class invokeWithReCaptcha(TLObject):
    token: str
    query: TLObject
    def __init__(self, *, token: str, query: TLObject) -> None: ...

class invokeWithTakeout(TLObject):
    takeout_id: int
    query: TLObject
    def __init__(self, *, takeout_id: int, query: TLObject) -> None: ...

class invokeWithoutUpdates(TLObject):
    query: TLObject
    def __init__(self, *, query: TLObject) -> None: ...

class joinChatBotResultApproved(TLObject):
    def __init__(self) -> None: ...

class joinChatBotResultDeclined(TLObject):
    def __init__(self) -> None: ...

class joinChatBotResultQueued(TLObject):
    def __init__(self) -> None: ...

class joinChatBotResultWebView(TLObject):
    url: str
    def __init__(self, *, url: str) -> None: ...

class jsonArray(TLObject):
    value: list[TLObject]
    def __init__(self, *, value: list[TLObject]) -> None: ...

class jsonBool(TLObject):
    value: bool
    def __init__(self, *, value: bool) -> None: ...

class jsonNull(TLObject):
    def __init__(self) -> None: ...

class jsonNumber(TLObject):
    value: float
    def __init__(self, *, value: float) -> None: ...

class jsonObject(TLObject):
    value: list[TLObject]
    def __init__(self, *, value: list[TLObject]) -> None: ...

class jsonObjectValue(TLObject):
    key: str
    value: TLObject
    def __init__(self, *, key: str, value: TLObject) -> None: ...

class jsonString(TLObject):
    value: str
    def __init__(self, *, value: str) -> None: ...

class keyboardButton(TLObject):
    style: TLObject | None
    text: str
    type: TLObject
    def __init__(self, *, style: TLObject | None = ..., text: str, type: TLObject) -> None: ...

class keyboardButtonRow(TLObject):
    buttons: list[TLObject]
    def __init__(self, *, buttons: list[TLObject]) -> None: ...

class keyboardButtonStyle(TLObject):
    bg_primary: bool
    bg_danger: bool
    bg_success: bool
    icon: int | None
    def __init__(self, *, bg_primary: bool = ..., bg_danger: bool = ..., bg_success: bool = ..., icon: int | None = ...) -> None: ...

class keyboardInlineButton(TLObject):
    style: TLObject | None
    text: str
    type: TLObject
    def __init__(self, *, style: TLObject | None = ..., text: str, type: TLObject) -> None: ...

class keyboardInlineButtonRow(TLObject):
    buttons: list[TLObject]
    def __init__(self, *, buttons: list[TLObject]) -> None: ...

class labeledPrice(TLObject):
    label: str
    amount: int
    def __init__(self, *, label: str, amount: int) -> None: ...

class langPackDifference(TLObject):
    lang_code: str
    from_version: int
    version: int
    strings: list[TLObject]
    def __init__(self, *, lang_code: str, from_version: int, version: int, strings: list[TLObject]) -> None: ...

class langPackLanguage(TLObject):
    official: bool
    rtl: bool
    beta: bool
    name: str
    native_name: str
    lang_code: str
    base_lang_code: str | None
    plural_code: str
    strings_count: int
    translated_count: int
    translations_url: str
    def __init__(self, *, official: bool = ..., rtl: bool = ..., beta: bool = ..., name: str, native_name: str, lang_code: str, base_lang_code: str | None = ..., plural_code: str, strings_count: int, translated_count: int, translations_url: str) -> None: ...

class langPackString(TLObject):
    key: str
    value: str
    def __init__(self, *, key: str, value: str) -> None: ...

class langPackStringDeleted(TLObject):
    key: str
    def __init__(self, *, key: str) -> None: ...

class langPackStringPluralized(TLObject):
    key: str
    zero_value: str | None
    one_value: str | None
    two_value: str | None
    few_value: str | None
    many_value: str | None
    other_value: str
    def __init__(self, *, key: str, zero_value: str | None = ..., one_value: str | None = ..., two_value: str | None = ..., few_value: str | None = ..., many_value: str | None = ..., other_value: str) -> None: ...

class langpack:
    class getDifference(TLObject):
        lang_pack: str
        lang_code: str
        from_version: int
        def __init__(self, *, lang_pack: str, lang_code: str, from_version: int) -> None: ...

    class getLangPack(TLObject):
        lang_pack: str
        lang_code: str
        def __init__(self, *, lang_pack: str, lang_code: str) -> None: ...

    class getLanguage(TLObject):
        lang_pack: str
        lang_code: str
        def __init__(self, *, lang_pack: str, lang_code: str) -> None: ...

    class getLanguages(TLObject):
        lang_pack: str
        def __init__(self, *, lang_pack: str) -> None: ...

    class getStrings(TLObject):
        lang_pack: str
        lang_code: str
        keys: list[str]
        def __init__(self, *, lang_pack: str, lang_code: str, keys: list[str]) -> None: ...

class maskCoords(TLObject):
    n: int
    x: float
    y: float
    zoom: float
    def __init__(self, *, n: int, x: float, y: float, zoom: float) -> None: ...

class mediaAreaChannelPost(TLObject):
    coordinates: TLObject
    channel_id: int
    msg_id: int
    def __init__(self, *, coordinates: TLObject, channel_id: int, msg_id: int) -> None: ...

class mediaAreaCoordinates(TLObject):
    x: float
    y: float
    w: float
    h: float
    rotation: float
    radius: float | None
    def __init__(self, *, x: float, y: float, w: float, h: float, rotation: float, radius: float | None = ...) -> None: ...

class mediaAreaGeoPoint(TLObject):
    coordinates: TLObject
    geo: TLObject
    address: TLObject | None
    def __init__(self, *, coordinates: TLObject, geo: TLObject, address: TLObject | None = ...) -> None: ...

class mediaAreaStarGift(TLObject):
    coordinates: TLObject
    slug: str
    def __init__(self, *, coordinates: TLObject, slug: str) -> None: ...

class mediaAreaSuggestedReaction(TLObject):
    dark: bool
    flipped: bool
    coordinates: TLObject
    reaction: TLObject
    def __init__(self, *, dark: bool = ..., flipped: bool = ..., coordinates: TLObject, reaction: TLObject) -> None: ...

class mediaAreaUrl(TLObject):
    coordinates: TLObject
    url: str
    def __init__(self, *, coordinates: TLObject, url: str) -> None: ...

class mediaAreaVenue(TLObject):
    coordinates: TLObject
    geo: TLObject
    title: str
    address: str
    provider: str
    venue_id: str
    venue_type: str
    def __init__(self, *, coordinates: TLObject, geo: TLObject, title: str, address: str, provider: str, venue_id: str, venue_type: str) -> None: ...

class mediaAreaWeather(TLObject):
    coordinates: TLObject
    emoji: str
    temperature_c: float
    color: int
    def __init__(self, *, coordinates: TLObject, emoji: str, temperature_c: float, color: int) -> None: ...

class message(TLObject):
    out: bool
    mentioned: bool
    media_unread: bool
    silent: bool
    post: bool
    from_scheduled: bool
    legacy: bool
    edit_hide: bool
    pinned: bool
    noforwards: bool
    invert_media: bool
    offline: bool
    video_processing_pending: bool
    paid_suggested_post_stars: bool
    paid_suggested_post_ton: bool
    id: int
    from_id: TLObject | None
    from_boosts_applied: int | None
    from_rank: str | None
    peer_id: TLObject
    saved_peer_id: TLObject | None
    fwd_from: TLObject | None
    via_bot_id: int | None
    via_business_bot_id: int | None
    guestchat_via_from: TLObject | None
    reply_to: TLObject | None
    date: int
    message: str
    media: TLObject | None
    reply_markup: TLObject | None
    entities: list[TLObject] | None
    views: int | None
    forwards: int | None
    replies: TLObject | None
    edit_date: int | None
    post_author: str | None
    grouped_id: int | None
    reactions: TLObject | None
    restriction_reason: list[TLObject] | None
    ttl_period: int | None
    quick_reply_shortcut_id: int | None
    effect: int | None
    factcheck: TLObject | None
    report_delivery_until_date: int | None
    paid_message_stars: int | None
    suggested_post: TLObject | None
    schedule_repeat_period: int | None
    summary_from_language: str | None
    rich_message: TLObject | None
    def __init__(self, *, out: bool = ..., mentioned: bool = ..., media_unread: bool = ..., silent: bool = ..., post: bool = ..., from_scheduled: bool = ..., legacy: bool = ..., edit_hide: bool = ..., pinned: bool = ..., noforwards: bool = ..., invert_media: bool = ..., offline: bool = ..., video_processing_pending: bool = ..., paid_suggested_post_stars: bool = ..., paid_suggested_post_ton: bool = ..., id: int, from_id: TLObject | None = ..., from_boosts_applied: int | None = ..., from_rank: str | None = ..., peer_id: TLObject, saved_peer_id: TLObject | None = ..., fwd_from: TLObject | None = ..., via_bot_id: int | None = ..., via_business_bot_id: int | None = ..., guestchat_via_from: TLObject | None = ..., reply_to: TLObject | None = ..., date: int, message: str, media: TLObject | None = ..., reply_markup: TLObject | None = ..., entities: list[TLObject] | None = ..., views: int | None = ..., forwards: int | None = ..., replies: TLObject | None = ..., edit_date: int | None = ..., post_author: str | None = ..., grouped_id: int | None = ..., reactions: TLObject | None = ..., restriction_reason: list[TLObject] | None = ..., ttl_period: int | None = ..., quick_reply_shortcut_id: int | None = ..., effect: int | None = ..., factcheck: TLObject | None = ..., report_delivery_until_date: int | None = ..., paid_message_stars: int | None = ..., suggested_post: TLObject | None = ..., schedule_repeat_period: int | None = ..., summary_from_language: str | None = ..., rich_message: TLObject | None = ...) -> None: ...

class messageActionBoostApply(TLObject):
    boosts: int
    def __init__(self, *, boosts: int) -> None: ...

class messageActionBotAllowed(TLObject):
    attach_menu: bool
    from_request: bool
    domain: str | None
    app: TLObject | None
    def __init__(self, *, attach_menu: bool = ..., from_request: bool = ..., domain: str | None = ..., app: TLObject | None = ...) -> None: ...

class messageActionChangeCommunity(TLObject):
    community_id: int | None
    def __init__(self, *, community_id: int | None = ...) -> None: ...

class messageActionChangeCreator(TLObject):
    new_creator_id: int
    def __init__(self, *, new_creator_id: int) -> None: ...

class messageActionChannelCreate(TLObject):
    title: str
    def __init__(self, *, title: str) -> None: ...

class messageActionChannelMigrateFrom(TLObject):
    title: str
    chat_id: int
    def __init__(self, *, title: str, chat_id: int) -> None: ...

class messageActionChatAddUser(TLObject):
    users: list[int]
    def __init__(self, *, users: list[int]) -> None: ...

class messageActionChatCreate(TLObject):
    title: str
    users: list[int]
    def __init__(self, *, title: str, users: list[int]) -> None: ...

class messageActionChatDeletePhoto(TLObject):
    def __init__(self) -> None: ...

class messageActionChatDeleteUser(TLObject):
    user_id: int
    def __init__(self, *, user_id: int) -> None: ...

class messageActionChatEditPhoto(TLObject):
    photo: TLObject
    def __init__(self, *, photo: TLObject) -> None: ...

class messageActionChatEditTitle(TLObject):
    title: str
    def __init__(self, *, title: str) -> None: ...

class messageActionChatJoinedByLink(TLObject):
    inviter_id: int
    def __init__(self, *, inviter_id: int) -> None: ...

class messageActionChatJoinedByRequest(TLObject):
    def __init__(self) -> None: ...

class messageActionChatJoinedViaCommunity(TLObject):
    community_id: int
    def __init__(self, *, community_id: int) -> None: ...

class messageActionChatMigrateTo(TLObject):
    channel_id: int
    def __init__(self, *, channel_id: int) -> None: ...

class messageActionConferenceCall(TLObject):
    missed: bool
    active: bool
    video: bool
    call_id: int
    duration: int | None
    other_participants: list[TLObject] | None
    def __init__(self, *, missed: bool = ..., active: bool = ..., video: bool = ..., call_id: int, duration: int | None = ..., other_participants: list[TLObject] | None = ...) -> None: ...

class messageActionContactSignUp(TLObject):
    def __init__(self) -> None: ...

class messageActionCustomAction(TLObject):
    message: str
    def __init__(self, *, message: str) -> None: ...

class messageActionEmpty(TLObject):
    def __init__(self) -> None: ...

class messageActionGameScore(TLObject):
    game_id: int
    score: int
    def __init__(self, *, game_id: int, score: int) -> None: ...

class messageActionGeoProximityReached(TLObject):
    from_id: TLObject
    to_id: TLObject
    distance: int
    def __init__(self, *, from_id: TLObject, to_id: TLObject, distance: int) -> None: ...

class messageActionGiftCode(TLObject):
    via_giveaway: bool
    unclaimed: bool
    boost_peer: TLObject | None
    days: int
    slug: str
    currency: str | None
    amount: int | None
    crypto_currency: str | None
    crypto_amount: int | None
    message: TLObject | None
    def __init__(self, *, via_giveaway: bool = ..., unclaimed: bool = ..., boost_peer: TLObject | None = ..., days: int, slug: str, currency: str | None = ..., amount: int | None = ..., crypto_currency: str | None = ..., crypto_amount: int | None = ..., message: TLObject | None = ...) -> None: ...

class messageActionGiftPremium(TLObject):
    currency: str
    amount: int
    days: int
    crypto_currency: str | None
    crypto_amount: int | None
    message: TLObject | None
    def __init__(self, *, currency: str, amount: int, days: int, crypto_currency: str | None = ..., crypto_amount: int | None = ..., message: TLObject | None = ...) -> None: ...

class messageActionGiftStars(TLObject):
    currency: str
    amount: int
    stars: int
    crypto_currency: str | None
    crypto_amount: int | None
    transaction_id: str | None
    def __init__(self, *, currency: str, amount: int, stars: int, crypto_currency: str | None = ..., crypto_amount: int | None = ..., transaction_id: str | None = ...) -> None: ...

class messageActionGiftTon(TLObject):
    currency: str
    amount: int
    crypto_currency: str
    crypto_amount: int
    transaction_id: str | None
    def __init__(self, *, currency: str, amount: int, crypto_currency: str, crypto_amount: int, transaction_id: str | None = ...) -> None: ...

class messageActionGiveawayLaunch(TLObject):
    stars: int | None
    def __init__(self, *, stars: int | None = ...) -> None: ...

class messageActionGiveawayResults(TLObject):
    stars: bool
    winners_count: int
    unclaimed_count: int
    def __init__(self, *, stars: bool = ..., winners_count: int, unclaimed_count: int) -> None: ...

class messageActionGramTransfer(TLObject):
    comment_encrypted: bool
    amount: int
    peer_address: str
    transaction_id: str
    comment: str | None
    def __init__(self, *, comment_encrypted: bool = ..., amount: int, peer_address: str, transaction_id: str, comment: str | None = ...) -> None: ...

class messageActionGroupCall(TLObject):
    call: TLObject
    duration: int | None
    def __init__(self, *, call: TLObject, duration: int | None = ...) -> None: ...

class messageActionGroupCallScheduled(TLObject):
    call: TLObject
    schedule_date: int
    def __init__(self, *, call: TLObject, schedule_date: int) -> None: ...

class messageActionHistoryClear(TLObject):
    def __init__(self) -> None: ...

class messageActionInviteToGroupCall(TLObject):
    call: TLObject
    users: list[int]
    def __init__(self, *, call: TLObject, users: list[int]) -> None: ...

class messageActionManagedBotCreated(TLObject):
    bot_id: int
    def __init__(self, *, bot_id: int) -> None: ...

class messageActionNewCreatorPending(TLObject):
    new_creator_id: int
    def __init__(self, *, new_creator_id: int) -> None: ...

class messageActionNoForwardsRequest(TLObject):
    expired: bool
    prev_value: bool
    new_value: bool
    def __init__(self, *, expired: bool = ..., prev_value: bool, new_value: bool) -> None: ...

class messageActionNoForwardsToggle(TLObject):
    prev_value: bool
    new_value: bool
    def __init__(self, *, prev_value: bool, new_value: bool) -> None: ...

class messageActionNoPaidMessagesTokenUsed(TLObject):
    def __init__(self) -> None: ...

class messageActionPaidMessagesPrice(TLObject):
    broadcast_messages_allowed: bool
    stars: int
    def __init__(self, *, broadcast_messages_allowed: bool = ..., stars: int) -> None: ...

class messageActionPaidMessagesRefunded(TLObject):
    count: int
    stars: int
    def __init__(self, *, count: int, stars: int) -> None: ...

class messageActionPaymentRefunded(TLObject):
    peer: TLObject
    currency: str
    total_amount: int
    payload: bytes | None
    charge: TLObject
    def __init__(self, *, peer: TLObject, currency: str, total_amount: int, payload: bytes | None = ..., charge: TLObject) -> None: ...

class messageActionPaymentSent(TLObject):
    recurring_init: bool
    recurring_used: bool
    currency: str
    total_amount: int
    invoice_slug: str | None
    subscription_until_date: int | None
    def __init__(self, *, recurring_init: bool = ..., recurring_used: bool = ..., currency: str, total_amount: int, invoice_slug: str | None = ..., subscription_until_date: int | None = ...) -> None: ...

class messageActionPaymentSentMe(TLObject):
    recurring_init: bool
    recurring_used: bool
    currency: str
    total_amount: int
    payload: bytes
    info: TLObject | None
    shipping_option_id: str | None
    charge: TLObject
    subscription_until_date: int | None
    def __init__(self, *, recurring_init: bool = ..., recurring_used: bool = ..., currency: str, total_amount: int, payload: bytes, info: TLObject | None = ..., shipping_option_id: str | None = ..., charge: TLObject, subscription_until_date: int | None = ...) -> None: ...

class messageActionPhoneCall(TLObject):
    video: bool
    call_id: int
    reason: TLObject | None
    duration: int | None
    def __init__(self, *, video: bool = ..., call_id: int, reason: TLObject | None = ..., duration: int | None = ...) -> None: ...

class messageActionPinMessage(TLObject):
    def __init__(self) -> None: ...

class messageActionPollAppendAnswer(TLObject):
    answer: TLObject
    def __init__(self, *, answer: TLObject) -> None: ...

class messageActionPollDeleteAnswer(TLObject):
    answer: TLObject
    def __init__(self, *, answer: TLObject) -> None: ...

class messageActionPrizeStars(TLObject):
    unclaimed: bool
    stars: int
    transaction_id: str
    boost_peer: TLObject
    giveaway_msg_id: int
    def __init__(self, *, unclaimed: bool = ..., stars: int, transaction_id: str, boost_peer: TLObject, giveaway_msg_id: int) -> None: ...

class messageActionRequestedPeer(TLObject):
    button_id: int
    peers: list[TLObject]
    def __init__(self, *, button_id: int, peers: list[TLObject]) -> None: ...

class messageActionRequestedPeerSentMe(TLObject):
    button_id: int
    peers: list[TLObject]
    def __init__(self, *, button_id: int, peers: list[TLObject]) -> None: ...

class messageActionScreenshotTaken(TLObject):
    def __init__(self) -> None: ...

class messageActionSecureValuesSent(TLObject):
    types: list[TLObject]
    def __init__(self, *, types: list[TLObject]) -> None: ...

class messageActionSecureValuesSentMe(TLObject):
    values: list[TLObject]
    credentials: TLObject
    def __init__(self, *, values: list[TLObject], credentials: TLObject) -> None: ...

class messageActionSetChatTheme(TLObject):
    theme: TLObject
    def __init__(self, *, theme: TLObject) -> None: ...

class messageActionSetChatWallPaper(TLObject):
    same: bool
    for_both: bool
    wallpaper: TLObject
    def __init__(self, *, same: bool = ..., for_both: bool = ..., wallpaper: TLObject) -> None: ...

class messageActionSetMessagesTTL(TLObject):
    period: int
    auto_setting_from: int | None
    def __init__(self, *, period: int, auto_setting_from: int | None = ...) -> None: ...

class messageActionStarGift(TLObject):
    name_hidden: bool
    saved: bool
    converted: bool
    upgraded: bool
    refunded: bool
    can_upgrade: bool
    prepaid_upgrade: bool
    upgrade_separate: bool
    auction_acquired: bool
    gift: TLObject
    message: TLObject | None
    convert_stars: int | None
    upgrade_msg_id: int | None
    upgrade_stars: int | None
    from_id: TLObject | None
    peer: TLObject | None
    saved_id: int | None
    prepaid_upgrade_hash: str | None
    gift_msg_id: int | None
    to_id: TLObject | None
    gift_num: int | None
    def __init__(self, *, name_hidden: bool = ..., saved: bool = ..., converted: bool = ..., upgraded: bool = ..., refunded: bool = ..., can_upgrade: bool = ..., prepaid_upgrade: bool = ..., upgrade_separate: bool = ..., auction_acquired: bool = ..., gift: TLObject, message: TLObject | None = ..., convert_stars: int | None = ..., upgrade_msg_id: int | None = ..., upgrade_stars: int | None = ..., from_id: TLObject | None = ..., peer: TLObject | None = ..., saved_id: int | None = ..., prepaid_upgrade_hash: str | None = ..., gift_msg_id: int | None = ..., to_id: TLObject | None = ..., gift_num: int | None = ...) -> None: ...

class messageActionStarGiftPurchaseOffer(TLObject):
    accepted: bool
    declined: bool
    gift: TLObject
    price: TLObject
    expires_at: int
    def __init__(self, *, accepted: bool = ..., declined: bool = ..., gift: TLObject, price: TLObject, expires_at: int) -> None: ...

class messageActionStarGiftPurchaseOfferDeclined(TLObject):
    expired: bool
    gift: TLObject
    price: TLObject
    def __init__(self, *, expired: bool = ..., gift: TLObject, price: TLObject) -> None: ...

class messageActionStarGiftUnique(TLObject):
    upgrade: bool
    transferred: bool
    saved: bool
    refunded: bool
    prepaid_upgrade: bool
    assigned: bool
    from_offer: bool
    craft: bool
    name_hidden: bool
    gift: TLObject
    can_export_at: int | None
    transfer_stars: int | None
    from_id: TLObject | None
    peer: TLObject | None
    saved_id: int | None
    resale_amount: TLObject | None
    can_transfer_at: int | None
    can_resell_at: int | None
    drop_original_details_stars: int | None
    can_craft_at: int | None
    message: TLObject | None
    def __init__(self, *, upgrade: bool = ..., transferred: bool = ..., saved: bool = ..., refunded: bool = ..., prepaid_upgrade: bool = ..., assigned: bool = ..., from_offer: bool = ..., craft: bool = ..., name_hidden: bool = ..., gift: TLObject, can_export_at: int | None = ..., transfer_stars: int | None = ..., from_id: TLObject | None = ..., peer: TLObject | None = ..., saved_id: int | None = ..., resale_amount: TLObject | None = ..., can_transfer_at: int | None = ..., can_resell_at: int | None = ..., drop_original_details_stars: int | None = ..., can_craft_at: int | None = ..., message: TLObject | None = ...) -> None: ...

class messageActionSuggestBirthday(TLObject):
    birthday: TLObject
    def __init__(self, *, birthday: TLObject) -> None: ...

class messageActionSuggestProfilePhoto(TLObject):
    photo: TLObject
    def __init__(self, *, photo: TLObject) -> None: ...

class messageActionSuggestedPostApproval(TLObject):
    rejected: bool
    balance_too_low: bool
    reject_comment: str | None
    schedule_date: int | None
    price: TLObject | None
    def __init__(self, *, rejected: bool = ..., balance_too_low: bool = ..., reject_comment: str | None = ..., schedule_date: int | None = ..., price: TLObject | None = ...) -> None: ...

class messageActionSuggestedPostRefund(TLObject):
    payer_initiated: bool
    def __init__(self, *, payer_initiated: bool = ...) -> None: ...

class messageActionSuggestedPostSuccess(TLObject):
    price: TLObject
    def __init__(self, *, price: TLObject) -> None: ...

class messageActionTodoAppendTasks(TLObject):
    list: list[TLObject]
    def __init__(self, *, list: list[TLObject]) -> None: ...

class messageActionTodoCompletions(TLObject):
    completed: list[int]
    incompleted: list[int]
    def __init__(self, *, completed: list[int], incompleted: list[int]) -> None: ...

class messageActionTopicCreate(TLObject):
    title_missing: bool
    title: str
    icon_color: int
    icon_emoji_id: int | None
    def __init__(self, *, title_missing: bool = ..., title: str, icon_color: int, icon_emoji_id: int | None = ...) -> None: ...

class messageActionTopicEdit(TLObject):
    title: str | None
    icon_emoji_id: int | None
    closed: bool
    hidden: bool
    def __init__(self, *, title: str | None = ..., icon_emoji_id: int | None = ..., closed: bool = ..., hidden: bool = ...) -> None: ...

class messageActionWalletTonConnectRequest(TLObject):
    accepted: bool
    declined: bool
    session_id: int
    expires: int
    topic: str | None
    trace_id: str | None
    dapp_name: str | None
    def __init__(self, *, accepted: bool = ..., declined: bool = ..., session_id: int, expires: int, topic: str | None = ..., trace_id: str | None = ..., dapp_name: str | None = ...) -> None: ...

class messageActionWebViewDataSent(TLObject):
    text: str
    def __init__(self, *, text: str) -> None: ...

class messageActionWebViewDataSentMe(TLObject):
    text: str
    data: str
    def __init__(self, *, text: str, data: str) -> None: ...

class messageEmpty(TLObject):
    id: int
    peer_id: TLObject | None
    def __init__(self, *, id: int, peer_id: TLObject | None = ...) -> None: ...

class messageEntityBankCard(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityBlockquote(TLObject):
    collapsed: bool
    offset: int
    length: int
    def __init__(self, *, collapsed: bool = ..., offset: int, length: int) -> None: ...

class messageEntityBold(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityBotCommand(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityCashtag(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityCode(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityCustomEmoji(TLObject):
    offset: int
    length: int
    document_id: int
    def __init__(self, *, offset: int, length: int, document_id: int) -> None: ...

class messageEntityDiffDelete(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityDiffInsert(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityDiffReplace(TLObject):
    offset: int
    length: int
    old_text: str
    def __init__(self, *, offset: int, length: int, old_text: str) -> None: ...

class messageEntityEmail(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityFormattedDate(TLObject):
    relative: bool
    short_time: bool
    long_time: bool
    short_date: bool
    long_date: bool
    day_of_week: bool
    offset: int
    length: int
    date: int
    def __init__(self, *, relative: bool = ..., short_time: bool = ..., long_time: bool = ..., short_date: bool = ..., long_date: bool = ..., day_of_week: bool = ..., offset: int, length: int, date: int) -> None: ...

class messageEntityHashtag(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityItalic(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityMention(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityMentionName(TLObject):
    offset: int
    length: int
    user_id: int
    def __init__(self, *, offset: int, length: int, user_id: int) -> None: ...

class messageEntityPhone(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityPre(TLObject):
    offset: int
    length: int
    language: str
    def __init__(self, *, offset: int, length: int, language: str) -> None: ...

class messageEntitySpoiler(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityStrike(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityTextUrl(TLObject):
    offset: int
    length: int
    url: str
    def __init__(self, *, offset: int, length: int, url: str) -> None: ...

class messageEntityTonAddress(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityUnderline(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityUnknown(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageEntityUrl(TLObject):
    offset: int
    length: int
    def __init__(self, *, offset: int, length: int) -> None: ...

class messageExtendedMedia(TLObject):
    media: TLObject
    def __init__(self, *, media: TLObject) -> None: ...

class messageExtendedMediaPreview(TLObject):
    w: int | None
    h: int | None
    thumb: TLObject | None
    video_duration: int | None
    def __init__(self, *, w: int | None = ..., h: int | None = ..., thumb: TLObject | None = ..., video_duration: int | None = ...) -> None: ...

class messageFwdHeader(TLObject):
    imported: bool
    saved_out: bool
    from_id: TLObject | None
    from_name: str | None
    date: int
    channel_post: int | None
    post_author: str | None
    saved_from_peer: TLObject | None
    saved_from_msg_id: int | None
    saved_from_id: TLObject | None
    saved_from_name: str | None
    saved_date: int | None
    psa_type: str | None
    def __init__(self, *, imported: bool = ..., saved_out: bool = ..., from_id: TLObject | None = ..., from_name: str | None = ..., date: int, channel_post: int | None = ..., post_author: str | None = ..., saved_from_peer: TLObject | None = ..., saved_from_msg_id: int | None = ..., saved_from_id: TLObject | None = ..., saved_from_name: str | None = ..., saved_date: int | None = ..., psa_type: str | None = ...) -> None: ...

class messageMediaContact(TLObject):
    phone_number: str
    first_name: str
    last_name: str
    vcard: str
    user_id: int
    def __init__(self, *, phone_number: str, first_name: str, last_name: str, vcard: str, user_id: int) -> None: ...

class messageMediaDice(TLObject):
    value: int
    emoticon: str
    game_outcome: TLObject | None
    def __init__(self, *, value: int, emoticon: str, game_outcome: TLObject | None = ...) -> None: ...

class messageMediaDocument(TLObject):
    nopremium: bool
    spoiler: bool
    video: bool
    round: bool
    voice: bool
    document: TLObject | None
    alt_documents: list[TLObject] | None
    video_cover: TLObject | None
    video_timestamp: int | None
    ttl_seconds: int | None
    def __init__(self, *, nopremium: bool = ..., spoiler: bool = ..., video: bool = ..., round: bool = ..., voice: bool = ..., document: TLObject | None = ..., alt_documents: list[TLObject] | None = ..., video_cover: TLObject | None = ..., video_timestamp: int | None = ..., ttl_seconds: int | None = ...) -> None: ...

class messageMediaEmpty(TLObject):
    def __init__(self) -> None: ...

class messageMediaGame(TLObject):
    game: TLObject
    def __init__(self, *, game: TLObject) -> None: ...

class messageMediaGeo(TLObject):
    geo: TLObject
    def __init__(self, *, geo: TLObject) -> None: ...

class messageMediaGeoLive(TLObject):
    geo: TLObject
    heading: int | None
    period: int
    proximity_notification_radius: int | None
    def __init__(self, *, geo: TLObject, heading: int | None = ..., period: int, proximity_notification_radius: int | None = ...) -> None: ...

class messageMediaGiveaway(TLObject):
    only_new_subscribers: bool
    winners_are_visible: bool
    channels: list[int]
    countries_iso2: list[str] | None
    prize_description: str | None
    quantity: int
    months: int | None
    stars: int | None
    until_date: int
    def __init__(self, *, only_new_subscribers: bool = ..., winners_are_visible: bool = ..., channels: list[int], countries_iso2: list[str] | None = ..., prize_description: str | None = ..., quantity: int, months: int | None = ..., stars: int | None = ..., until_date: int) -> None: ...

class messageMediaGiveawayResults(TLObject):
    only_new_subscribers: bool
    refunded: bool
    channel_id: int
    additional_peers_count: int | None
    launch_msg_id: int
    winners_count: int
    unclaimed_count: int
    winners: list[int]
    months: int | None
    stars: int | None
    prize_description: str | None
    until_date: int
    def __init__(self, *, only_new_subscribers: bool = ..., refunded: bool = ..., channel_id: int, additional_peers_count: int | None = ..., launch_msg_id: int, winners_count: int, unclaimed_count: int, winners: list[int], months: int | None = ..., stars: int | None = ..., prize_description: str | None = ..., until_date: int) -> None: ...

class messageMediaInvoice(TLObject):
    shipping_address_requested: bool
    test: bool
    title: str
    description: str
    photo: TLObject | None
    receipt_msg_id: int | None
    currency: str
    total_amount: int
    start_param: str
    extended_media: TLObject | None
    def __init__(self, *, shipping_address_requested: bool = ..., test: bool = ..., title: str, description: str, photo: TLObject | None = ..., receipt_msg_id: int | None = ..., currency: str, total_amount: int, start_param: str, extended_media: TLObject | None = ...) -> None: ...

class messageMediaPaidMedia(TLObject):
    stars_amount: int
    extended_media: list[TLObject]
    def __init__(self, *, stars_amount: int, extended_media: list[TLObject]) -> None: ...

class messageMediaPhoto(TLObject):
    spoiler: bool
    live_photo: bool
    photo: TLObject | None
    ttl_seconds: int | None
    video: TLObject | None
    def __init__(self, *, spoiler: bool = ..., live_photo: bool = ..., photo: TLObject | None = ..., ttl_seconds: int | None = ..., video: TLObject | None = ...) -> None: ...

class messageMediaPoll(TLObject):
    poll: TLObject
    results: TLObject
    attached_media: TLObject | None
    def __init__(self, *, poll: TLObject, results: TLObject, attached_media: TLObject | None = ...) -> None: ...

class messageMediaStory(TLObject):
    via_mention: bool
    peer: TLObject
    id: int
    story: TLObject | None
    def __init__(self, *, via_mention: bool = ..., peer: TLObject, id: int, story: TLObject | None = ...) -> None: ...

class messageMediaToDo(TLObject):
    todo: TLObject
    completions: list[TLObject] | None
    def __init__(self, *, todo: TLObject, completions: list[TLObject] | None = ...) -> None: ...

class messageMediaUnsupported(TLObject):
    def __init__(self) -> None: ...

class messageMediaVenue(TLObject):
    geo: TLObject
    title: str
    address: str
    provider: str
    venue_id: str
    venue_type: str
    def __init__(self, *, geo: TLObject, title: str, address: str, provider: str, venue_id: str, venue_type: str) -> None: ...

class messageMediaVideoStream(TLObject):
    rtmp_stream: bool
    call: TLObject
    def __init__(self, *, rtmp_stream: bool = ..., call: TLObject) -> None: ...

class messageMediaWebPage(TLObject):
    force_large_media: bool
    force_small_media: bool
    manual: bool
    safe: bool
    webpage: TLObject
    def __init__(self, *, force_large_media: bool = ..., force_small_media: bool = ..., manual: bool = ..., safe: bool = ..., webpage: TLObject) -> None: ...

class messageMediaWidget(TLObject):
    is_copy: bool
    can_query: bool
    background_query: bool
    width: int
    height: int
    payload: bytes
    public_data: str | None
    public_data_hash: int | None
    chat_data: str | None
    widget_id: int | None
    def __init__(self, *, is_copy: bool = ..., can_query: bool = ..., background_query: bool = ..., width: int, height: int, payload: bytes, public_data: str | None = ..., public_data_hash: int | None = ..., chat_data: str | None = ..., widget_id: int | None = ...) -> None: ...

class messagePeerReaction(TLObject):
    big: bool
    unread: bool
    my: bool
    peer_id: TLObject
    date: int
    reaction: TLObject
    def __init__(self, *, big: bool = ..., unread: bool = ..., my: bool = ..., peer_id: TLObject, date: int, reaction: TLObject) -> None: ...

class messagePeerVote(TLObject):
    peer: TLObject
    option: bytes
    date: int
    def __init__(self, *, peer: TLObject, option: bytes, date: int) -> None: ...

class messagePeerVoteInputOption(TLObject):
    peer: TLObject
    date: int
    def __init__(self, *, peer: TLObject, date: int) -> None: ...

class messagePeerVoteMultiple(TLObject):
    peer: TLObject
    options: list[bytes]
    date: int
    def __init__(self, *, peer: TLObject, options: list[bytes], date: int) -> None: ...

class messageRange(TLObject):
    min_id: int
    max_id: int
    def __init__(self, *, min_id: int, max_id: int) -> None: ...

class messageReactions(TLObject):
    min: bool
    can_see_list: bool
    reactions_as_tags: bool
    results: list[TLObject]
    recent_reactions: list[TLObject] | None
    top_reactors: list[TLObject] | None
    def __init__(self, *, min: bool = ..., can_see_list: bool = ..., reactions_as_tags: bool = ..., results: list[TLObject], recent_reactions: list[TLObject] | None = ..., top_reactors: list[TLObject] | None = ...) -> None: ...

class messageReactor(TLObject):
    top: bool
    my: bool
    anonymous: bool
    peer_id: TLObject | None
    count: int
    def __init__(self, *, top: bool = ..., my: bool = ..., anonymous: bool = ..., peer_id: TLObject | None = ..., count: int) -> None: ...

class messageReplies(TLObject):
    comments: bool
    replies: int
    replies_pts: int
    recent_repliers: list[TLObject] | None
    channel_id: int | None
    max_id: int | None
    read_max_id: int | None
    def __init__(self, *, comments: bool = ..., replies: int, replies_pts: int, recent_repliers: list[TLObject] | None = ..., channel_id: int | None = ..., max_id: int | None = ..., read_max_id: int | None = ...) -> None: ...

class messageReplyHeader(TLObject):
    reply_to_scheduled: bool
    forum_topic: bool
    quote: bool
    reply_to_ephemeral: bool
    reply_to_msg_id: int | None
    reply_to_peer_id: TLObject | None
    reply_from: TLObject | None
    reply_media: TLObject | None
    reply_to_top_id: int | None
    quote_text: str | None
    quote_entities: list[TLObject] | None
    quote_offset: int | None
    todo_item_id: int | None
    poll_option: bytes | None
    quote_rich: list[TLObject] | None
    def __init__(self, *, reply_to_scheduled: bool = ..., forum_topic: bool = ..., quote: bool = ..., reply_to_ephemeral: bool = ..., reply_to_msg_id: int | None = ..., reply_to_peer_id: TLObject | None = ..., reply_from: TLObject | None = ..., reply_media: TLObject | None = ..., reply_to_top_id: int | None = ..., quote_text: str | None = ..., quote_entities: list[TLObject] | None = ..., quote_offset: int | None = ..., todo_item_id: int | None = ..., poll_option: bytes | None = ..., quote_rich: list[TLObject] | None = ...) -> None: ...

class messageReplyStoryHeader(TLObject):
    peer: TLObject
    story_id: int
    def __init__(self, *, peer: TLObject, story_id: int) -> None: ...

class messageReportOption(TLObject):
    text: str
    option: bytes
    def __init__(self, *, text: str, option: bytes) -> None: ...

class messageService(TLObject):
    out: bool
    mentioned: bool
    media_unread: bool
    reactions_are_possible: bool
    silent: bool
    post: bool
    legacy: bool
    id: int
    from_id: TLObject | None
    peer_id: TLObject
    saved_peer_id: TLObject | None
    reply_to: TLObject | None
    date: int
    action: TLObject
    reactions: TLObject | None
    ttl_period: int | None
    def __init__(self, *, out: bool = ..., mentioned: bool = ..., media_unread: bool = ..., reactions_are_possible: bool = ..., silent: bool = ..., post: bool = ..., legacy: bool = ..., id: int, from_id: TLObject | None = ..., peer_id: TLObject, saved_peer_id: TLObject | None = ..., reply_to: TLObject | None = ..., date: int, action: TLObject, reactions: TLObject | None = ..., ttl_period: int | None = ...) -> None: ...

class messageViews(TLObject):
    views: int | None
    forwards: int | None
    replies: TLObject | None
    def __init__(self, *, views: int | None = ..., forwards: int | None = ..., replies: TLObject | None = ...) -> None: ...

class messages:
    class acceptEncryption(TLObject):
        peer: TLObject
        g_b: bytes
        key_fingerprint: int
        def __init__(self, *, peer: TLObject, g_b: bytes, key_fingerprint: int) -> None: ...

    class acceptUrlAuth(TLObject):
        write_allowed: bool
        share_phone_number: bool
        peer: TLObject | None
        msg_id: int | None
        button_id: int | None
        url: str | None
        match_code: str | None
        tonconnect_session: TLObject | None
        def __init__(self, *, write_allowed: bool = ..., share_phone_number: bool = ..., peer: TLObject | None = ..., msg_id: int | None = ..., button_id: int | None = ..., url: str | None = ..., match_code: str | None = ..., tonconnect_session: TLObject | None = ...) -> None: ...

    class addChatUser(TLObject):
        chat_id: int
        user_id: TLObject
        fwd_limit: int
        def __init__(self, *, chat_id: int, user_id: TLObject, fwd_limit: int) -> None: ...

    class addPollAnswer(TLObject):
        peer: TLObject
        msg_id: int
        answer: TLObject
        def __init__(self, *, peer: TLObject, msg_id: int, answer: TLObject) -> None: ...

    class affectedFoundMessages(TLObject):
        pts: int
        pts_count: int
        offset: int
        messages: list[int]
        def __init__(self, *, pts: int, pts_count: int, offset: int, messages: list[int]) -> None: ...

    class affectedHistory(TLObject):
        pts: int
        pts_count: int
        offset: int
        def __init__(self, *, pts: int, pts_count: int, offset: int) -> None: ...

    class affectedMessages(TLObject):
        pts: int
        pts_count: int
        def __init__(self, *, pts: int, pts_count: int) -> None: ...

    class allStickers(TLObject):
        hash: int
        sets: list[TLObject]
        def __init__(self, *, hash: int, sets: list[TLObject]) -> None: ...

    class allStickersNotModified(TLObject):
        def __init__(self) -> None: ...

    class appendTodoList(TLObject):
        peer: TLObject
        msg_id: int
        list: list[TLObject]
        def __init__(self, *, peer: TLObject, msg_id: int, list: list[TLObject]) -> None: ...

    class archivedStickers(TLObject):
        count: int
        sets: list[TLObject]
        def __init__(self, *, count: int, sets: list[TLObject]) -> None: ...

    class availableEffects(TLObject):
        hash: int
        effects: list[TLObject]
        documents: list[TLObject]
        def __init__(self, *, hash: int, effects: list[TLObject], documents: list[TLObject]) -> None: ...

    class availableEffectsNotModified(TLObject):
        def __init__(self) -> None: ...

    class availableReactions(TLObject):
        hash: int
        reactions: list[TLObject]
        def __init__(self, *, hash: int, reactions: list[TLObject]) -> None: ...

    class availableReactionsNotModified(TLObject):
        def __init__(self) -> None: ...

    class botApp(TLObject):
        inactive: bool
        request_write_access: bool
        has_settings: bool
        app: TLObject
        def __init__(self, *, inactive: bool = ..., request_write_access: bool = ..., has_settings: bool = ..., app: TLObject) -> None: ...

    class botCallbackAnswer(TLObject):
        alert: bool
        has_url: bool
        native_ui: bool
        message: str | None
        url: str | None
        cache_time: int
        def __init__(self, *, alert: bool = ..., has_url: bool = ..., native_ui: bool = ..., message: str | None = ..., url: str | None = ..., cache_time: int) -> None: ...

    class botPreparedInlineMessage(TLObject):
        id: str
        expire_date: int
        def __init__(self, *, id: str, expire_date: int) -> None: ...

    class botResults(TLObject):
        gallery: bool
        query_id: int
        next_offset: str | None
        switch_pm: TLObject | None
        switch_webview: TLObject | None
        results: list[TLObject]
        cache_time: int
        users: list[TLObject]
        def __init__(self, *, gallery: bool = ..., query_id: int, next_offset: str | None = ..., switch_pm: TLObject | None = ..., switch_webview: TLObject | None = ..., results: list[TLObject], cache_time: int, users: list[TLObject]) -> None: ...

    class botWidgetQueryAnswer(TLObject):
        result: str | None
        def __init__(self, *, result: str | None = ...) -> None: ...

    class channelMessages(TLObject):
        inexact: bool
        pts: int
        count: int
        offset_id_offset: int | None
        messages: list[TLObject]
        topics: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, inexact: bool = ..., pts: int, count: int, offset_id_offset: int | None = ..., messages: list[TLObject], topics: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class chatAdminsWithInvites(TLObject):
        admins: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, admins: list[TLObject], users: list[TLObject]) -> None: ...

    class chatFull(TLObject):
        full_chat: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, full_chat: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class chatInviteImporters(TLObject):
        count: int
        importers: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, importers: list[TLObject], users: list[TLObject]) -> None: ...

    class chatInviteJoinResultOk(TLObject):
        updates: TLObject
        def __init__(self, *, updates: TLObject) -> None: ...

    class chatInviteJoinResultWebView(TLObject):
        bot_id: int
        query_id: int
        users: list[TLObject]
        def __init__(self, *, bot_id: int, query_id: int, users: list[TLObject]) -> None: ...

    class chats(TLObject):
        chats: list[TLObject]
        def __init__(self, *, chats: list[TLObject]) -> None: ...

    class chatsSlice(TLObject):
        count: int
        chats: list[TLObject]
        def __init__(self, *, count: int, chats: list[TLObject]) -> None: ...

    class checkChatInvite(TLObject):
        hash: str
        def __init__(self, *, hash: str) -> None: ...

    class checkHistoryImport(TLObject):
        import_head: str
        def __init__(self, *, import_head: str) -> None: ...

    class checkHistoryImportPeer(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class checkQuickReplyShortcut(TLObject):
        shortcut: str
        def __init__(self, *, shortcut: str) -> None: ...

    class checkUrlAuthMatchCode(TLObject):
        url: str
        match_code: str
        def __init__(self, *, url: str, match_code: str) -> None: ...

    class checkedHistoryImportPeer(TLObject):
        confirm_text: str
        def __init__(self, *, confirm_text: str) -> None: ...

    class clearAllDrafts(TLObject):
        def __init__(self) -> None: ...

    class clearRecentReactions(TLObject):
        def __init__(self) -> None: ...

    class clearRecentStickers(TLObject):
        attached: bool
        def __init__(self, *, attached: bool = ...) -> None: ...

    class clickSponsoredMessage(TLObject):
        media: bool
        fullscreen: bool
        random_id: bytes
        def __init__(self, *, media: bool = ..., fullscreen: bool = ..., random_id: bytes) -> None: ...

    class composeMessageWithAI(TLObject):
        proofread: bool
        emojify: bool
        text: TLObject
        translate_to_lang: str | None
        tone: TLObject | None
        def __init__(self, *, proofread: bool = ..., emojify: bool = ..., text: TLObject, translate_to_lang: str | None = ..., tone: TLObject | None = ...) -> None: ...

    class composeRichMessageWithAI(TLObject):
        proofread: bool
        emojify: bool
        text: TLObject | None
        translate_to_lang: str | None
        tone: TLObject | None
        def __init__(self, *, proofread: bool = ..., emojify: bool = ..., text: TLObject | None = ..., translate_to_lang: str | None = ..., tone: TLObject | None = ...) -> None: ...

    class composedMessageWithAI(TLObject):
        result_text: TLObject
        diff_text: TLObject | None
        def __init__(self, *, result_text: TLObject, diff_text: TLObject | None = ...) -> None: ...

    class composedRichMessageWithAI(TLObject):
        result: TLObject
        def __init__(self, *, result: TLObject) -> None: ...

    class createChat(TLObject):
        users: list[TLObject]
        title: str
        ttl_period: int | None
        def __init__(self, *, users: list[TLObject], title: str, ttl_period: int | None = ...) -> None: ...

    class createForumTopic(TLObject):
        title_missing: bool
        peer: TLObject
        title: str
        icon_color: int | None
        icon_emoji_id: int | None
        random_id: int
        send_as: TLObject | None
        def __init__(self, *, title_missing: bool = ..., peer: TLObject, title: str, icon_color: int | None = ..., icon_emoji_id: int | None = ..., random_id: int, send_as: TLObject | None = ...) -> None: ...

    class declineUrlAuth(TLObject):
        url: str
        def __init__(self, *, url: str) -> None: ...

    class deleteChat(TLObject):
        chat_id: int
        def __init__(self, *, chat_id: int) -> None: ...

    class deleteChatUser(TLObject):
        revoke_history: bool
        chat_id: int
        user_id: TLObject
        def __init__(self, *, revoke_history: bool = ..., chat_id: int, user_id: TLObject) -> None: ...

    class deleteExportedChatInvite(TLObject):
        peer: TLObject
        link: str
        def __init__(self, *, peer: TLObject, link: str) -> None: ...

    class deleteFactCheck(TLObject):
        peer: TLObject
        msg_id: int
        def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

    class deleteHistory(TLObject):
        just_clear: bool
        revoke: bool
        peer: TLObject
        max_id: int
        min_date: int | None
        max_date: int | None
        def __init__(self, *, just_clear: bool = ..., revoke: bool = ..., peer: TLObject, max_id: int, min_date: int | None = ..., max_date: int | None = ...) -> None: ...

    class deleteMessages(TLObject):
        revoke: bool
        id: list[int]
        def __init__(self, *, revoke: bool = ..., id: list[int]) -> None: ...

    class deleteParticipantReaction(TLObject):
        peer: TLObject
        msg_id: int
        participant: TLObject
        def __init__(self, *, peer: TLObject, msg_id: int, participant: TLObject) -> None: ...

    class deleteParticipantReactions(TLObject):
        peer: TLObject
        participant: TLObject
        def __init__(self, *, peer: TLObject, participant: TLObject) -> None: ...

    class deletePhoneCallHistory(TLObject):
        revoke: bool
        def __init__(self, *, revoke: bool = ...) -> None: ...

    class deletePollAnswer(TLObject):
        peer: TLObject
        msg_id: int
        option: bytes
        def __init__(self, *, peer: TLObject, msg_id: int, option: bytes) -> None: ...

    class deleteQuickReplyMessages(TLObject):
        shortcut_id: int
        id: list[int]
        def __init__(self, *, shortcut_id: int, id: list[int]) -> None: ...

    class deleteQuickReplyShortcut(TLObject):
        shortcut_id: int
        def __init__(self, *, shortcut_id: int) -> None: ...

    class deleteRevokedExportedChatInvites(TLObject):
        peer: TLObject
        admin_id: TLObject
        def __init__(self, *, peer: TLObject, admin_id: TLObject) -> None: ...

    class deleteSavedHistory(TLObject):
        parent_peer: TLObject | None
        peer: TLObject
        max_id: int
        min_date: int | None
        max_date: int | None
        def __init__(self, *, parent_peer: TLObject | None = ..., peer: TLObject, max_id: int, min_date: int | None = ..., max_date: int | None = ...) -> None: ...

    class deleteScheduledMessages(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class deleteTopicHistory(TLObject):
        peer: TLObject
        top_msg_id: int
        def __init__(self, *, peer: TLObject, top_msg_id: int) -> None: ...

    class dhConfig(TLObject):
        g: int
        p: bytes
        version: int
        random: bytes
        def __init__(self, *, g: int, p: bytes, version: int, random: bytes) -> None: ...

    class dhConfigNotModified(TLObject):
        random: bytes
        def __init__(self, *, random: bytes) -> None: ...

    class dialogFilters(TLObject):
        tags_enabled: bool
        filters: list[TLObject]
        def __init__(self, *, tags_enabled: bool = ..., filters: list[TLObject]) -> None: ...

    class dialogs(TLObject):
        dialogs: list[TLObject]
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, dialogs: list[TLObject], messages: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class dialogsNotModified(TLObject):
        count: int
        def __init__(self, *, count: int) -> None: ...

    class dialogsSlice(TLObject):
        count: int
        dialogs: list[TLObject]
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, dialogs: list[TLObject], messages: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class discardEncryption(TLObject):
        delete_history: bool
        chat_id: int
        def __init__(self, *, delete_history: bool = ..., chat_id: int) -> None: ...

    class discussionMessage(TLObject):
        messages: list[TLObject]
        max_id: int | None
        read_inbox_max_id: int | None
        read_outbox_max_id: int | None
        unread_count: int
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, messages: list[TLObject], max_id: int | None = ..., read_inbox_max_id: int | None = ..., read_outbox_max_id: int | None = ..., unread_count: int, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class editChatAbout(TLObject):
        peer: TLObject
        about: str
        def __init__(self, *, peer: TLObject, about: str) -> None: ...

    class editChatAdmin(TLObject):
        chat_id: int
        user_id: TLObject
        is_admin: bool
        def __init__(self, *, chat_id: int, user_id: TLObject, is_admin: bool) -> None: ...

    class editChatCreator(TLObject):
        peer: TLObject
        user_id: TLObject
        password: TLObject
        def __init__(self, *, peer: TLObject, user_id: TLObject, password: TLObject) -> None: ...

    class editChatDefaultBannedRights(TLObject):
        peer: TLObject
        banned_rights: TLObject
        def __init__(self, *, peer: TLObject, banned_rights: TLObject) -> None: ...

    class editChatParticipantRank(TLObject):
        peer: TLObject
        participant: TLObject
        rank: str
        def __init__(self, *, peer: TLObject, participant: TLObject, rank: str) -> None: ...

    class editChatPhoto(TLObject):
        chat_id: int
        photo: TLObject
        def __init__(self, *, chat_id: int, photo: TLObject) -> None: ...

    class editChatTitle(TLObject):
        chat_id: int
        title: str
        def __init__(self, *, chat_id: int, title: str) -> None: ...

    class editExportedChatInvite(TLObject):
        revoked: bool
        peer: TLObject
        link: str
        expire_date: int | None
        usage_limit: int | None
        request_needed: bool
        title: str | None
        def __init__(self, *, revoked: bool = ..., peer: TLObject, link: str, expire_date: int | None = ..., usage_limit: int | None = ..., request_needed: bool = ..., title: str | None = ...) -> None: ...

    class editFactCheck(TLObject):
        peer: TLObject
        msg_id: int
        text: TLObject
        def __init__(self, *, peer: TLObject, msg_id: int, text: TLObject) -> None: ...

    class editForumTopic(TLObject):
        peer: TLObject
        topic_id: int
        title: str | None
        icon_emoji_id: int | None
        closed: bool
        hidden: bool
        def __init__(self, *, peer: TLObject, topic_id: int, title: str | None = ..., icon_emoji_id: int | None = ..., closed: bool = ..., hidden: bool = ...) -> None: ...

    class editInlineBotMessage(TLObject):
        no_webpage: bool
        invert_media: bool
        id: TLObject
        message: str | None
        media: TLObject | None
        reply_markup: TLObject | None
        entities: list[TLObject] | None
        rich_message: TLObject | None
        def __init__(self, *, no_webpage: bool = ..., invert_media: bool = ..., id: TLObject, message: str | None = ..., media: TLObject | None = ..., reply_markup: TLObject | None = ..., entities: list[TLObject] | None = ..., rich_message: TLObject | None = ...) -> None: ...

    class editInlineBotMessageWidgetData(TLObject):
        id: TLObject
        public_data: str | None
        chat_data: str | None
        def __init__(self, *, id: TLObject, public_data: str | None = ..., chat_data: str | None = ...) -> None: ...

    class editMessage(TLObject):
        no_webpage: bool
        invert_media: bool
        peer: TLObject
        id: int
        message: str | None
        media: TLObject | None
        reply_markup: TLObject | None
        entities: list[TLObject] | None
        schedule_date: int | None
        schedule_repeat_period: int | None
        quick_reply_shortcut_id: int | None
        rich_message: TLObject | None
        def __init__(self, *, no_webpage: bool = ..., invert_media: bool = ..., peer: TLObject, id: int, message: str | None = ..., media: TLObject | None = ..., reply_markup: TLObject | None = ..., entities: list[TLObject] | None = ..., schedule_date: int | None = ..., schedule_repeat_period: int | None = ..., quick_reply_shortcut_id: int | None = ..., rich_message: TLObject | None = ...) -> None: ...

    class editMessageWidgetData(TLObject):
        peer: TLObject
        id: int
        public_data: str | None
        chat_data: str | None
        def __init__(self, *, peer: TLObject, id: int, public_data: str | None = ..., chat_data: str | None = ...) -> None: ...

    class editQuickReplyShortcut(TLObject):
        shortcut_id: int
        shortcut: str
        def __init__(self, *, shortcut_id: int, shortcut: str) -> None: ...

    class editWidgetData(TLObject):
        widget_id: int
        public_data: str
        cache_time: int | None
        def __init__(self, *, widget_id: int, public_data: str, cache_time: int | None = ...) -> None: ...

    class emojiGameDiceInfo(TLObject):
        game_hash: str
        prev_stake: int
        current_streak: int
        params: list[int]
        plays_left: int | None
        def __init__(self, *, game_hash: str, prev_stake: int, current_streak: int, params: list[int], plays_left: int | None = ...) -> None: ...

    class emojiGameOutcome(TLObject):
        seed: bytes
        stake_ton_amount: int
        ton_amount: int
        def __init__(self, *, seed: bytes, stake_ton_amount: int, ton_amount: int) -> None: ...

    class emojiGameUnavailable(TLObject):
        def __init__(self) -> None: ...

    class emojiGroups(TLObject):
        hash: int
        groups: list[TLObject]
        def __init__(self, *, hash: int, groups: list[TLObject]) -> None: ...

    class emojiGroupsNotModified(TLObject):
        def __init__(self) -> None: ...

    class exportChatInvite(TLObject):
        legacy_revoke_permanent: bool
        request_needed: bool
        peer: TLObject
        expire_date: int | None
        usage_limit: int | None
        title: str | None
        subscription_pricing: TLObject | None
        def __init__(self, *, legacy_revoke_permanent: bool = ..., request_needed: bool = ..., peer: TLObject, expire_date: int | None = ..., usage_limit: int | None = ..., title: str | None = ..., subscription_pricing: TLObject | None = ...) -> None: ...

    class exportedChatInvite(TLObject):
        invite: TLObject
        users: list[TLObject]
        def __init__(self, *, invite: TLObject, users: list[TLObject]) -> None: ...

    class exportedChatInviteReplaced(TLObject):
        invite: TLObject
        new_invite: TLObject
        users: list[TLObject]
        def __init__(self, *, invite: TLObject, new_invite: TLObject, users: list[TLObject]) -> None: ...

    class exportedChatInvites(TLObject):
        count: int
        invites: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, invites: list[TLObject], users: list[TLObject]) -> None: ...

    class faveSticker(TLObject):
        id: TLObject
        unfave: bool
        def __init__(self, *, id: TLObject, unfave: bool) -> None: ...

    class favedStickers(TLObject):
        hash: int
        packs: list[TLObject]
        stickers: list[TLObject]
        def __init__(self, *, hash: int, packs: list[TLObject], stickers: list[TLObject]) -> None: ...

    class favedStickersNotModified(TLObject):
        def __init__(self) -> None: ...

    class featuredStickers(TLObject):
        premium: bool
        hash: int
        count: int
        sets: list[TLObject]
        unread: list[int]
        def __init__(self, *, premium: bool = ..., hash: int, count: int, sets: list[TLObject], unread: list[int]) -> None: ...

    class featuredStickersNotModified(TLObject):
        count: int
        def __init__(self, *, count: int) -> None: ...

    class forumTopics(TLObject):
        order_by_create_date: bool
        count: int
        topics: list[TLObject]
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        pts: int
        def __init__(self, *, order_by_create_date: bool = ..., count: int, topics: list[TLObject], messages: list[TLObject], chats: list[TLObject], users: list[TLObject], pts: int) -> None: ...

    class forwardMessages(TLObject):
        silent: bool
        background: bool
        with_my_score: bool
        drop_author: bool
        drop_media_captions: bool
        noforwards: bool
        allow_paid_floodskip: bool
        from_ephemeral: bool
        from_peer: TLObject
        id: list[int]
        random_id: list[int]
        to_peer: TLObject
        top_msg_id: int | None
        reply_to: TLObject | None
        schedule_date: int | None
        schedule_repeat_period: int | None
        send_as: TLObject | None
        quick_reply_shortcut: TLObject | None
        effect: int | None
        video_timestamp: int | None
        allow_paid_stars: int | None
        suggested_post: TLObject | None
        def __init__(self, *, silent: bool = ..., background: bool = ..., with_my_score: bool = ..., drop_author: bool = ..., drop_media_captions: bool = ..., noforwards: bool = ..., allow_paid_floodskip: bool = ..., from_ephemeral: bool = ..., from_peer: TLObject, id: list[int], random_id: list[int], to_peer: TLObject, top_msg_id: int | None = ..., reply_to: TLObject | None = ..., schedule_date: int | None = ..., schedule_repeat_period: int | None = ..., send_as: TLObject | None = ..., quick_reply_shortcut: TLObject | None = ..., effect: int | None = ..., video_timestamp: int | None = ..., allow_paid_stars: int | None = ..., suggested_post: TLObject | None = ...) -> None: ...

    class foundStickerSets(TLObject):
        hash: int
        sets: list[TLObject]
        def __init__(self, *, hash: int, sets: list[TLObject]) -> None: ...

    class foundStickerSetsNotModified(TLObject):
        def __init__(self) -> None: ...

    class foundStickers(TLObject):
        next_offset: int | None
        hash: int
        stickers: list[TLObject]
        def __init__(self, *, next_offset: int | None = ..., hash: int, stickers: list[TLObject]) -> None: ...

    class foundStickersNotModified(TLObject):
        next_offset: int | None
        def __init__(self, *, next_offset: int | None = ...) -> None: ...

    class getAdminsWithInvites(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getAllDrafts(TLObject):
        def __init__(self) -> None: ...

    class getAllStickers(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getArchivedStickers(TLObject):
        masks: bool
        emojis: bool
        offset_id: int
        limit: int
        def __init__(self, *, masks: bool = ..., emojis: bool = ..., offset_id: int, limit: int) -> None: ...

    class getAttachMenuBot(TLObject):
        bot: TLObject
        def __init__(self, *, bot: TLObject) -> None: ...

    class getAttachMenuBots(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getAttachedStickers(TLObject):
        media: TLObject
        def __init__(self, *, media: TLObject) -> None: ...

    class getAvailableEffects(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getAvailableReactions(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getBotApp(TLObject):
        app: TLObject
        hash: int
        def __init__(self, *, app: TLObject, hash: int) -> None: ...

    class getBotCallbackAnswer(TLObject):
        game: bool
        peer: TLObject
        msg_id: int
        data: bytes | None
        password: TLObject | None
        def __init__(self, *, game: bool = ..., peer: TLObject, msg_id: int, data: bytes | None = ..., password: TLObject | None = ...) -> None: ...

    class getBotWidgetQueryAnswer(TLObject):
        peer: TLObject
        msg_id: int
        query_type: TLObject
        data: bytes
        def __init__(self, *, peer: TLObject, msg_id: int, query_type: TLObject, data: bytes) -> None: ...

    class getChatInviteImporters(TLObject):
        requested: bool
        subscription_expired: bool
        peer: TLObject
        link: str | None
        q: str | None
        offset_date: int
        offset_user: TLObject
        limit: int
        def __init__(self, *, requested: bool = ..., subscription_expired: bool = ..., peer: TLObject, link: str | None = ..., q: str | None = ..., offset_date: int, offset_user: TLObject, limit: int) -> None: ...

    class getChats(TLObject):
        id: list[int]
        def __init__(self, *, id: list[int]) -> None: ...

    class getCommonChats(TLObject):
        user_id: TLObject
        max_id: int
        limit: int
        def __init__(self, *, user_id: TLObject, max_id: int, limit: int) -> None: ...

    class getCustomEmojiDocuments(TLObject):
        document_id: list[int]
        def __init__(self, *, document_id: list[int]) -> None: ...

    class getDefaultHistoryTTL(TLObject):
        def __init__(self) -> None: ...

    class getDefaultTagReactions(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getDhConfig(TLObject):
        version: int
        random_length: int
        def __init__(self, *, version: int, random_length: int) -> None: ...

    class getDialogFilters(TLObject):
        def __init__(self) -> None: ...

    class getDialogUnreadMarks(TLObject):
        parent_peer: TLObject | None
        def __init__(self, *, parent_peer: TLObject | None = ...) -> None: ...

    class getDialogs(TLObject):
        exclude_pinned: bool
        folder_id: int | None
        offset_date: int
        offset_id: int
        offset_peer: TLObject
        limit: int
        hash: int
        def __init__(self, *, exclude_pinned: bool = ..., folder_id: int | None = ..., offset_date: int, offset_id: int, offset_peer: TLObject, limit: int, hash: int) -> None: ...

    class getDiscussionMessage(TLObject):
        peer: TLObject
        msg_id: int
        def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

    class getDocumentByHash(TLObject):
        sha256: bytes
        size: int
        mime_type: str
        def __init__(self, *, sha256: bytes, size: int, mime_type: str) -> None: ...

    class getEmojiGameInfo(TLObject):
        def __init__(self) -> None: ...

    class getEmojiGroups(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getEmojiKeywords(TLObject):
        lang_code: str
        def __init__(self, *, lang_code: str) -> None: ...

    class getEmojiKeywordsDifference(TLObject):
        lang_code: str
        from_version: int
        def __init__(self, *, lang_code: str, from_version: int) -> None: ...

    class getEmojiKeywordsLanguages(TLObject):
        lang_codes: list[str]
        def __init__(self, *, lang_codes: list[str]) -> None: ...

    class getEmojiProfilePhotoGroups(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getEmojiStatusGroups(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getEmojiStickerGroups(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getEmojiStickers(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getEmojiURL(TLObject):
        lang_code: str
        def __init__(self, *, lang_code: str) -> None: ...

    class getExportedChatInvite(TLObject):
        peer: TLObject
        link: str
        def __init__(self, *, peer: TLObject, link: str) -> None: ...

    class getExportedChatInvites(TLObject):
        revoked: bool
        peer: TLObject
        admin_id: TLObject
        offset_date: int | None
        offset_link: str | None
        limit: int
        def __init__(self, *, revoked: bool = ..., peer: TLObject, admin_id: TLObject, offset_date: int | None = ..., offset_link: str | None = ..., limit: int) -> None: ...

    class getExtendedMedia(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class getFactCheck(TLObject):
        peer: TLObject
        msg_id: list[int]
        def __init__(self, *, peer: TLObject, msg_id: list[int]) -> None: ...

    class getFavedStickers(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getFeaturedEmojiStickers(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getFeaturedStickers(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getForumTopics(TLObject):
        peer: TLObject
        q: str | None
        offset_date: int
        offset_id: int
        offset_topic: int
        limit: int
        def __init__(self, *, peer: TLObject, q: str | None = ..., offset_date: int, offset_id: int, offset_topic: int, limit: int) -> None: ...

    class getForumTopicsByID(TLObject):
        peer: TLObject
        topics: list[int]
        def __init__(self, *, peer: TLObject, topics: list[int]) -> None: ...

    class getFullChat(TLObject):
        chat_id: int
        def __init__(self, *, chat_id: int) -> None: ...

    class getFutureChatCreatorAfterLeave(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getGameHighScores(TLObject):
        peer: TLObject
        id: int
        user_id: TLObject
        def __init__(self, *, peer: TLObject, id: int, user_id: TLObject) -> None: ...

    class getHistory(TLObject):
        peer: TLObject
        offset_id: int
        offset_date: int
        add_offset: int
        limit: int
        max_id: int
        min_id: int
        hash: int
        def __init__(self, *, peer: TLObject, offset_id: int, offset_date: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int) -> None: ...

    class getInlineBotResults(TLObject):
        bot: TLObject
        peer: TLObject
        geo_point: TLObject | None
        query: str
        offset: str
        def __init__(self, *, bot: TLObject, peer: TLObject, geo_point: TLObject | None = ..., query: str, offset: str) -> None: ...

    class getInlineGameHighScores(TLObject):
        id: TLObject
        user_id: TLObject
        def __init__(self, *, id: TLObject, user_id: TLObject) -> None: ...

    class getMaskStickers(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getMessageEditData(TLObject):
        peer: TLObject
        id: int
        def __init__(self, *, peer: TLObject, id: int) -> None: ...

    class getMessageReactionsList(TLObject):
        peer: TLObject
        id: int
        reaction: TLObject | None
        offset: str | None
        limit: int
        def __init__(self, *, peer: TLObject, id: int, reaction: TLObject | None = ..., offset: str | None = ..., limit: int) -> None: ...

    class getMessageReadParticipants(TLObject):
        peer: TLObject
        msg_id: int
        def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

    class getMessages(TLObject):
        id: list[TLObject]
        def __init__(self, *, id: list[TLObject]) -> None: ...

    class getMessagesReactions(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class getMessagesViews(TLObject):
        peer: TLObject
        id: list[int]
        increment: bool
        def __init__(self, *, peer: TLObject, id: list[int], increment: bool) -> None: ...

    class getMyStickers(TLObject):
        offset_id: int
        limit: int
        def __init__(self, *, offset_id: int, limit: int) -> None: ...

    class getOldFeaturedStickers(TLObject):
        offset: int
        limit: int
        hash: int
        def __init__(self, *, offset: int, limit: int, hash: int) -> None: ...

    class getOnlines(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getOutboxReadDate(TLObject):
        peer: TLObject
        msg_id: int
        def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

    class getPaidReactionPrivacy(TLObject):
        def __init__(self) -> None: ...

    class getPeerDialogs(TLObject):
        peers: list[TLObject]
        def __init__(self, *, peers: list[TLObject]) -> None: ...

    class getPeerSettings(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getPersonalChannelHistory(TLObject):
        user_id: TLObject
        limit: int
        max_id: int
        min_id: int
        hash: int
        def __init__(self, *, user_id: TLObject, limit: int, max_id: int, min_id: int, hash: int) -> None: ...

    class getPinnedDialogs(TLObject):
        folder_id: int
        def __init__(self, *, folder_id: int) -> None: ...

    class getPinnedSavedDialogs(TLObject):
        def __init__(self) -> None: ...

    class getPollResults(TLObject):
        peer: TLObject
        msg_id: int
        poll_hash: int
        def __init__(self, *, peer: TLObject, msg_id: int, poll_hash: int) -> None: ...

    class getPollVotes(TLObject):
        peer: TLObject
        id: int
        option: bytes | None
        offset: str | None
        limit: int
        def __init__(self, *, peer: TLObject, id: int, option: bytes | None = ..., offset: str | None = ..., limit: int) -> None: ...

    class getPreparedInlineMessage(TLObject):
        bot: TLObject
        id: str
        def __init__(self, *, bot: TLObject, id: str) -> None: ...

    class getQuickReplies(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getQuickReplyMessages(TLObject):
        shortcut_id: int
        id: list[int] | None
        hash: int
        def __init__(self, *, shortcut_id: int, id: list[int] | None = ..., hash: int) -> None: ...

    class getRecentLocations(TLObject):
        peer: TLObject
        limit: int
        hash: int
        def __init__(self, *, peer: TLObject, limit: int, hash: int) -> None: ...

    class getRecentReactions(TLObject):
        limit: int
        hash: int
        def __init__(self, *, limit: int, hash: int) -> None: ...

    class getRecentStickers(TLObject):
        attached: bool
        hash: int
        def __init__(self, *, attached: bool = ..., hash: int) -> None: ...

    class getReplies(TLObject):
        peer: TLObject
        msg_id: int
        offset_id: int
        offset_date: int
        add_offset: int
        limit: int
        max_id: int
        min_id: int
        hash: int
        def __init__(self, *, peer: TLObject, msg_id: int, offset_id: int, offset_date: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int) -> None: ...

    class getRichMessage(TLObject):
        peer: TLObject
        id: int
        def __init__(self, *, peer: TLObject, id: int) -> None: ...

    class getSavedDialogs(TLObject):
        exclude_pinned: bool
        parent_peer: TLObject | None
        offset_date: int
        offset_id: int
        offset_peer: TLObject
        limit: int
        hash: int
        def __init__(self, *, exclude_pinned: bool = ..., parent_peer: TLObject | None = ..., offset_date: int, offset_id: int, offset_peer: TLObject, limit: int, hash: int) -> None: ...

    class getSavedDialogsByID(TLObject):
        parent_peer: TLObject | None
        ids: list[TLObject]
        def __init__(self, *, parent_peer: TLObject | None = ..., ids: list[TLObject]) -> None: ...

    class getSavedGifs(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getSavedHistory(TLObject):
        parent_peer: TLObject | None
        peer: TLObject
        offset_id: int
        offset_date: int
        add_offset: int
        limit: int
        max_id: int
        min_id: int
        hash: int
        def __init__(self, *, parent_peer: TLObject | None = ..., peer: TLObject, offset_id: int, offset_date: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int) -> None: ...

    class getSavedReactionTags(TLObject):
        peer: TLObject | None
        hash: int
        def __init__(self, *, peer: TLObject | None = ..., hash: int) -> None: ...

    class getScheduledHistory(TLObject):
        peer: TLObject
        hash: int
        def __init__(self, *, peer: TLObject, hash: int) -> None: ...

    class getScheduledMessages(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class getSearchCounters(TLObject):
        peer: TLObject
        saved_peer_id: TLObject | None
        top_msg_id: int | None
        filters: list[TLObject]
        def __init__(self, *, peer: TLObject, saved_peer_id: TLObject | None = ..., top_msg_id: int | None = ..., filters: list[TLObject]) -> None: ...

    class getSearchResultsCalendar(TLObject):
        peer: TLObject
        saved_peer_id: TLObject | None
        filter: TLObject
        offset_id: int
        offset_date: int
        def __init__(self, *, peer: TLObject, saved_peer_id: TLObject | None = ..., filter: TLObject, offset_id: int, offset_date: int) -> None: ...

    class getSearchResultsPositions(TLObject):
        peer: TLObject
        saved_peer_id: TLObject | None
        filter: TLObject
        offset_id: int
        limit: int
        def __init__(self, *, peer: TLObject, saved_peer_id: TLObject | None = ..., filter: TLObject, offset_id: int, limit: int) -> None: ...

    class getShareThemeBackdrops(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getSplitRanges(TLObject):
        def __init__(self) -> None: ...

    class getSponsoredMessages(TLObject):
        peer: TLObject
        msg_id: int | None
        def __init__(self, *, peer: TLObject, msg_id: int | None = ...) -> None: ...

    class getStickerSet(TLObject):
        stickerset: TLObject
        hash: int
        def __init__(self, *, stickerset: TLObject, hash: int) -> None: ...

    class getStickers(TLObject):
        emoticon: str
        hash: int
        def __init__(self, *, emoticon: str, hash: int) -> None: ...

    class getSuggestedDialogFilters(TLObject):
        def __init__(self) -> None: ...

    class getTopReactions(TLObject):
        limit: int
        hash: int
        def __init__(self, *, limit: int, hash: int) -> None: ...

    class getTranscriptionLangs(TLObject):
        peer: TLObject | None
        def __init__(self, *, peer: TLObject | None = ...) -> None: ...

    class getUnreadMentions(TLObject):
        peer: TLObject
        top_msg_id: int | None
        offset_id: int
        add_offset: int
        limit: int
        max_id: int
        min_id: int
        def __init__(self, *, peer: TLObject, top_msg_id: int | None = ..., offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int) -> None: ...

    class getUnreadPollVotes(TLObject):
        peer: TLObject
        top_msg_id: int | None
        offset_id: int
        add_offset: int
        limit: int
        max_id: int
        min_id: int
        def __init__(self, *, peer: TLObject, top_msg_id: int | None = ..., offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int) -> None: ...

    class getUnreadReactions(TLObject):
        peer: TLObject
        top_msg_id: int | None
        saved_peer_id: TLObject | None
        offset_id: int
        add_offset: int
        limit: int
        max_id: int
        min_id: int
        def __init__(self, *, peer: TLObject, top_msg_id: int | None = ..., saved_peer_id: TLObject | None = ..., offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int) -> None: ...

    class getWebPage(TLObject):
        url: str
        hash: int
        def __init__(self, *, url: str, hash: int) -> None: ...

    class getWebPagePreview(TLObject):
        message: str
        entities: list[TLObject] | None
        def __init__(self, *, message: str, entities: list[TLObject] | None = ...) -> None: ...

    class getWidgetPublicData(TLObject):
        peer: TLObject
        msg_id: int
        hash: int
        def __init__(self, *, peer: TLObject, msg_id: int, hash: int) -> None: ...

    class hideAllChatJoinRequests(TLObject):
        approved: bool
        peer: TLObject
        link: str | None
        def __init__(self, *, approved: bool = ..., peer: TLObject, link: str | None = ...) -> None: ...

    class hideChatJoinRequest(TLObject):
        approved: bool
        peer: TLObject
        user_id: TLObject
        def __init__(self, *, approved: bool = ..., peer: TLObject, user_id: TLObject) -> None: ...

    class hidePeerSettingsBar(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class highScores(TLObject):
        scores: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, scores: list[TLObject], users: list[TLObject]) -> None: ...

    class historyImport(TLObject):
        id: int
        def __init__(self, *, id: int) -> None: ...

    class historyImportParsed(TLObject):
        pm: bool
        group: bool
        title: str | None
        def __init__(self, *, pm: bool = ..., group: bool = ..., title: str | None = ...) -> None: ...

    class importChatInvite(TLObject):
        hash: str
        def __init__(self, *, hash: str) -> None: ...

    class inactiveChats(TLObject):
        dates: list[int]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, dates: list[int], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class initHistoryImport(TLObject):
        peer: TLObject
        file: TLObject
        media_count: int
        def __init__(self, *, peer: TLObject, file: TLObject, media_count: int) -> None: ...

    class installStickerSet(TLObject):
        stickerset: TLObject
        archived: bool
        def __init__(self, *, stickerset: TLObject, archived: bool) -> None: ...

    class invitedUsers(TLObject):
        updates: TLObject
        missing_invitees: list[TLObject]
        def __init__(self, *, updates: TLObject, missing_invitees: list[TLObject]) -> None: ...

    class markDialogUnread(TLObject):
        unread: bool
        parent_peer: TLObject | None
        peer: TLObject
        def __init__(self, *, unread: bool = ..., parent_peer: TLObject | None = ..., peer: TLObject) -> None: ...

    class messageEditData(TLObject):
        caption: bool
        def __init__(self, *, caption: bool = ...) -> None: ...

    class messageReactionsList(TLObject):
        count: int
        reactions: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        next_offset: str | None
        def __init__(self, *, count: int, reactions: list[TLObject], chats: list[TLObject], users: list[TLObject], next_offset: str | None = ...) -> None: ...

    class messageViews(TLObject):
        views: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, views: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class messages(TLObject):
        messages: list[TLObject]
        topics: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, messages: list[TLObject], topics: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class messagesNotModified(TLObject):
        count: int
        def __init__(self, *, count: int) -> None: ...

    class messagesSlice(TLObject):
        inexact: bool
        count: int
        next_rate: int | None
        offset_id_offset: int | None
        search_flood: TLObject | None
        messages: list[TLObject]
        topics: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, inexact: bool = ..., count: int, next_rate: int | None = ..., offset_id_offset: int | None = ..., search_flood: TLObject | None = ..., messages: list[TLObject], topics: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class migrateChat(TLObject):
        chat_id: int
        def __init__(self, *, chat_id: int) -> None: ...

    class myStickers(TLObject):
        count: int
        sets: list[TLObject]
        def __init__(self, *, count: int, sets: list[TLObject]) -> None: ...

    class peerDialogs(TLObject):
        dialogs: list[TLObject]
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        state: TLObject
        def __init__(self, *, dialogs: list[TLObject], messages: list[TLObject], chats: list[TLObject], users: list[TLObject], state: TLObject) -> None: ...

    class peerSettings(TLObject):
        settings: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, settings: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class preparedInlineMessage(TLObject):
        query_id: int
        result: TLObject
        peer_types: list[TLObject]
        cache_time: int
        users: list[TLObject]
        def __init__(self, *, query_id: int, result: TLObject, peer_types: list[TLObject], cache_time: int, users: list[TLObject]) -> None: ...

    class prolongWebView(TLObject):
        silent: bool
        peer: TLObject
        bot: TLObject
        query_id: int
        reply_to: TLObject | None
        send_as: TLObject | None
        def __init__(self, *, silent: bool = ..., peer: TLObject, bot: TLObject, query_id: int, reply_to: TLObject | None = ..., send_as: TLObject | None = ...) -> None: ...

    class quickReplies(TLObject):
        quick_replies: list[TLObject]
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, quick_replies: list[TLObject], messages: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class quickRepliesNotModified(TLObject):
        def __init__(self) -> None: ...

    class rateTranscribedAudio(TLObject):
        peer: TLObject
        msg_id: int
        transcription_id: int
        good: bool
        def __init__(self, *, peer: TLObject, msg_id: int, transcription_id: int, good: bool) -> None: ...

    class reactions(TLObject):
        hash: int
        reactions: list[TLObject]
        def __init__(self, *, hash: int, reactions: list[TLObject]) -> None: ...

    class reactionsNotModified(TLObject):
        def __init__(self) -> None: ...

    class readDiscussion(TLObject):
        peer: TLObject
        msg_id: int
        read_max_id: int
        def __init__(self, *, peer: TLObject, msg_id: int, read_max_id: int) -> None: ...

    class readEncryptedHistory(TLObject):
        peer: TLObject
        max_date: int
        def __init__(self, *, peer: TLObject, max_date: int) -> None: ...

    class readFeaturedStickers(TLObject):
        id: list[int]
        def __init__(self, *, id: list[int]) -> None: ...

    class readHistory(TLObject):
        peer: TLObject
        max_id: int
        def __init__(self, *, peer: TLObject, max_id: int) -> None: ...

    class readMentions(TLObject):
        peer: TLObject
        top_msg_id: int | None
        def __init__(self, *, peer: TLObject, top_msg_id: int | None = ...) -> None: ...

    class readMessageContents(TLObject):
        id: list[int]
        def __init__(self, *, id: list[int]) -> None: ...

    class readPollVotes(TLObject):
        peer: TLObject
        top_msg_id: int | None
        def __init__(self, *, peer: TLObject, top_msg_id: int | None = ...) -> None: ...

    class readReactions(TLObject):
        peer: TLObject
        top_msg_id: int | None
        saved_peer_id: TLObject | None
        def __init__(self, *, peer: TLObject, top_msg_id: int | None = ..., saved_peer_id: TLObject | None = ...) -> None: ...

    class readSavedHistory(TLObject):
        parent_peer: TLObject
        peer: TLObject
        max_id: int
        def __init__(self, *, parent_peer: TLObject, peer: TLObject, max_id: int) -> None: ...

    class receivedMessages(TLObject):
        max_id: int
        def __init__(self, *, max_id: int) -> None: ...

    class receivedQueue(TLObject):
        max_qts: int
        def __init__(self, *, max_qts: int) -> None: ...

    class recentStickers(TLObject):
        hash: int
        packs: list[TLObject]
        stickers: list[TLObject]
        dates: list[int]
        def __init__(self, *, hash: int, packs: list[TLObject], stickers: list[TLObject], dates: list[int]) -> None: ...

    class recentStickersNotModified(TLObject):
        def __init__(self) -> None: ...

    class reorderPinnedDialogs(TLObject):
        force: bool
        folder_id: int
        order: list[TLObject]
        def __init__(self, *, force: bool = ..., folder_id: int, order: list[TLObject]) -> None: ...

    class reorderPinnedForumTopics(TLObject):
        force: bool
        peer: TLObject
        order: list[int]
        def __init__(self, *, force: bool = ..., peer: TLObject, order: list[int]) -> None: ...

    class reorderPinnedSavedDialogs(TLObject):
        force: bool
        order: list[TLObject]
        def __init__(self, *, force: bool = ..., order: list[TLObject]) -> None: ...

    class reorderQuickReplies(TLObject):
        order: list[int]
        def __init__(self, *, order: list[int]) -> None: ...

    class reorderStickerSets(TLObject):
        masks: bool
        emojis: bool
        order: list[int]
        def __init__(self, *, masks: bool = ..., emojis: bool = ..., order: list[int]) -> None: ...

    class report(TLObject):
        peer: TLObject
        id: list[int]
        option: bytes
        message: str
        def __init__(self, *, peer: TLObject, id: list[int], option: bytes, message: str) -> None: ...

    class reportEncryptedSpam(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class reportMessagesDelivery(TLObject):
        push: bool
        peer: TLObject
        id: list[int]
        def __init__(self, *, push: bool = ..., peer: TLObject, id: list[int]) -> None: ...

    class reportMusicListen(TLObject):
        id: TLObject
        listened_duration: int
        def __init__(self, *, id: TLObject, listened_duration: int) -> None: ...

    class reportReaction(TLObject):
        peer: TLObject
        id: int
        reaction_peer: TLObject
        def __init__(self, *, peer: TLObject, id: int, reaction_peer: TLObject) -> None: ...

    class reportReadMetrics(TLObject):
        peer: TLObject
        metrics: list[TLObject]
        def __init__(self, *, peer: TLObject, metrics: list[TLObject]) -> None: ...

    class reportSpam(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class reportSponsoredMessage(TLObject):
        random_id: bytes
        option: bytes
        def __init__(self, *, random_id: bytes, option: bytes) -> None: ...

    class requestAppWebView(TLObject):
        write_allowed: bool
        compact: bool
        fullscreen: bool
        peer: TLObject
        app: TLObject
        start_param: str | None
        theme_params: TLObject | None
        platform: str
        def __init__(self, *, write_allowed: bool = ..., compact: bool = ..., fullscreen: bool = ..., peer: TLObject, app: TLObject, start_param: str | None = ..., theme_params: TLObject | None = ..., platform: str) -> None: ...

    class requestChatJoinWebView(TLObject):
        query_id: int
        theme_params: TLObject | None
        platform: str
        def __init__(self, *, query_id: int, theme_params: TLObject | None = ..., platform: str) -> None: ...

    class requestEncryption(TLObject):
        user_id: TLObject
        random_id: int
        g_a: bytes
        def __init__(self, *, user_id: TLObject, random_id: int, g_a: bytes) -> None: ...

    class requestMainWebView(TLObject):
        compact: bool
        fullscreen: bool
        peer: TLObject
        bot: TLObject
        start_param: str | None
        theme_params: TLObject | None
        platform: str
        def __init__(self, *, compact: bool = ..., fullscreen: bool = ..., peer: TLObject, bot: TLObject, start_param: str | None = ..., theme_params: TLObject | None = ..., platform: str) -> None: ...

    class requestSimpleWebView(TLObject):
        from_switch_webview: bool
        from_side_menu: bool
        compact: bool
        fullscreen: bool
        bot: TLObject
        url: str | None
        start_param: str | None
        theme_params: TLObject | None
        platform: str
        def __init__(self, *, from_switch_webview: bool = ..., from_side_menu: bool = ..., compact: bool = ..., fullscreen: bool = ..., bot: TLObject, url: str | None = ..., start_param: str | None = ..., theme_params: TLObject | None = ..., platform: str) -> None: ...

    class requestUrlAuth(TLObject):
        peer: TLObject | None
        msg_id: int | None
        button_id: int | None
        url: str | None
        in_app_origin: str | None
        def __init__(self, *, peer: TLObject | None = ..., msg_id: int | None = ..., button_id: int | None = ..., url: str | None = ..., in_app_origin: str | None = ...) -> None: ...

    class requestWebView(TLObject):
        from_bot_menu: bool
        silent: bool
        compact: bool
        fullscreen: bool
        peer: TLObject
        bot: TLObject
        url: str | None
        start_param: str | None
        theme_params: TLObject | None
        platform: str
        reply_to: TLObject | None
        send_as: TLObject | None
        def __init__(self, *, from_bot_menu: bool = ..., silent: bool = ..., compact: bool = ..., fullscreen: bool = ..., peer: TLObject, bot: TLObject, url: str | None = ..., start_param: str | None = ..., theme_params: TLObject | None = ..., platform: str, reply_to: TLObject | None = ..., send_as: TLObject | None = ...) -> None: ...

    class saveDefaultSendAs(TLObject):
        peer: TLObject
        send_as: TLObject
        def __init__(self, *, peer: TLObject, send_as: TLObject) -> None: ...

    class saveDraft(TLObject):
        no_webpage: bool
        invert_media: bool
        reply_to: TLObject | None
        peer: TLObject
        message: str
        entities: list[TLObject] | None
        media: TLObject | None
        effect: int | None
        suggested_post: TLObject | None
        rich_message: TLObject | None
        def __init__(self, *, no_webpage: bool = ..., invert_media: bool = ..., reply_to: TLObject | None = ..., peer: TLObject, message: str, entities: list[TLObject] | None = ..., media: TLObject | None = ..., effect: int | None = ..., suggested_post: TLObject | None = ..., rich_message: TLObject | None = ...) -> None: ...

    class saveGif(TLObject):
        id: TLObject
        unsave: bool
        def __init__(self, *, id: TLObject, unsave: bool) -> None: ...

    class savePreparedInlineMessage(TLObject):
        result: TLObject
        user_id: TLObject
        peer_types: list[TLObject] | None
        def __init__(self, *, result: TLObject, user_id: TLObject, peer_types: list[TLObject] | None = ...) -> None: ...

    class saveRecentSticker(TLObject):
        attached: bool
        id: TLObject
        unsave: bool
        def __init__(self, *, attached: bool = ..., id: TLObject, unsave: bool) -> None: ...

    class savedDialogs(TLObject):
        dialogs: list[TLObject]
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, dialogs: list[TLObject], messages: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class savedDialogsNotModified(TLObject):
        count: int
        def __init__(self, *, count: int) -> None: ...

    class savedDialogsSlice(TLObject):
        count: int
        dialogs: list[TLObject]
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, dialogs: list[TLObject], messages: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class savedGifs(TLObject):
        hash: int
        gifs: list[TLObject]
        def __init__(self, *, hash: int, gifs: list[TLObject]) -> None: ...

    class savedGifsNotModified(TLObject):
        def __init__(self) -> None: ...

    class savedReactionTags(TLObject):
        tags: list[TLObject]
        hash: int
        def __init__(self, *, tags: list[TLObject], hash: int) -> None: ...

    class savedReactionTagsNotModified(TLObject):
        def __init__(self) -> None: ...

    class search(TLObject):
        peer: TLObject
        q: str
        from_id: TLObject | None
        saved_peer_id: TLObject | None
        saved_reaction: list[TLObject] | None
        top_msg_id: int | None
        filter: TLObject
        min_date: int
        max_date: int
        offset_id: int
        add_offset: int
        limit: int
        max_id: int
        min_id: int
        hash: int
        def __init__(self, *, peer: TLObject, q: str, from_id: TLObject | None = ..., saved_peer_id: TLObject | None = ..., saved_reaction: list[TLObject] | None = ..., top_msg_id: int | None = ..., filter: TLObject, min_date: int, max_date: int, offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int) -> None: ...

    class searchCounter(TLObject):
        inexact: bool
        filter: TLObject
        count: int
        def __init__(self, *, inexact: bool = ..., filter: TLObject, count: int) -> None: ...

    class searchCustomEmoji(TLObject):
        emoticon: str
        hash: int
        def __init__(self, *, emoticon: str, hash: int) -> None: ...

    class searchEmojiStickerSets(TLObject):
        exclude_featured: bool
        q: str
        hash: int
        def __init__(self, *, exclude_featured: bool = ..., q: str, hash: int) -> None: ...

    class searchGlobal(TLObject):
        broadcasts_only: bool
        groups_only: bool
        users_only: bool
        folder_id: int | None
        community: TLObject | None
        q: str
        filter: TLObject
        min_date: int
        max_date: int
        offset_rate: int
        offset_peer: TLObject
        offset_id: int
        limit: int
        def __init__(self, *, broadcasts_only: bool = ..., groups_only: bool = ..., users_only: bool = ..., folder_id: int | None = ..., community: TLObject | None = ..., q: str, filter: TLObject, min_date: int, max_date: int, offset_rate: int, offset_peer: TLObject, offset_id: int, limit: int) -> None: ...

    class searchResultsCalendar(TLObject):
        inexact: bool
        count: int
        min_date: int
        min_msg_id: int
        offset_id_offset: int | None
        periods: list[TLObject]
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, inexact: bool = ..., count: int, min_date: int, min_msg_id: int, offset_id_offset: int | None = ..., periods: list[TLObject], messages: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class searchResultsPositions(TLObject):
        count: int
        positions: list[TLObject]
        def __init__(self, *, count: int, positions: list[TLObject]) -> None: ...

    class searchSentMedia(TLObject):
        q: str
        filter: TLObject
        limit: int
        def __init__(self, *, q: str, filter: TLObject, limit: int) -> None: ...

    class searchStickerSets(TLObject):
        exclude_featured: bool
        q: str
        hash: int
        def __init__(self, *, exclude_featured: bool = ..., q: str, hash: int) -> None: ...

    class searchStickers(TLObject):
        emojis: bool
        q: str
        emoticon: str
        lang_code: list[str]
        offset: int
        limit: int
        hash: int
        def __init__(self, *, emojis: bool = ..., q: str, emoticon: str, lang_code: list[str], offset: int, limit: int, hash: int) -> None: ...

    class sendBotRequestedPeer(TLObject):
        peer: TLObject
        msg_id: int | None
        webapp_req_id: str | None
        button_id: int
        requested_peers: list[TLObject]
        def __init__(self, *, peer: TLObject, msg_id: int | None = ..., webapp_req_id: str | None = ..., button_id: int, requested_peers: list[TLObject]) -> None: ...

    class sendEncrypted(TLObject):
        silent: bool
        peer: TLObject
        random_id: int
        data: bytes
        def __init__(self, *, silent: bool = ..., peer: TLObject, random_id: int, data: bytes) -> None: ...

    class sendEncryptedFile(TLObject):
        silent: bool
        peer: TLObject
        random_id: int
        data: bytes
        file: TLObject
        def __init__(self, *, silent: bool = ..., peer: TLObject, random_id: int, data: bytes, file: TLObject) -> None: ...

    class sendEncryptedService(TLObject):
        peer: TLObject
        random_id: int
        data: bytes
        def __init__(self, *, peer: TLObject, random_id: int, data: bytes) -> None: ...

    class sendInlineBotResult(TLObject):
        silent: bool
        background: bool
        clear_draft: bool
        hide_via: bool
        peer: TLObject
        reply_to: TLObject | None
        random_id: int
        query_id: int
        id: str
        schedule_date: int | None
        send_as: TLObject | None
        quick_reply_shortcut: TLObject | None
        allow_paid_stars: int | None
        def __init__(self, *, silent: bool = ..., background: bool = ..., clear_draft: bool = ..., hide_via: bool = ..., peer: TLObject, reply_to: TLObject | None = ..., random_id: int, query_id: int, id: str, schedule_date: int | None = ..., send_as: TLObject | None = ..., quick_reply_shortcut: TLObject | None = ..., allow_paid_stars: int | None = ...) -> None: ...

    class sendMedia(TLObject):
        silent: bool
        background: bool
        clear_draft: bool
        noforwards: bool
        update_stickersets_order: bool
        invert_media: bool
        allow_paid_floodskip: bool
        peer: TLObject
        reply_to: TLObject | None
        media: TLObject
        message: str
        random_id: int
        reply_markup: TLObject | None
        entities: list[TLObject] | None
        schedule_date: int | None
        schedule_repeat_period: int | None
        send_as: TLObject | None
        quick_reply_shortcut: TLObject | None
        effect: int | None
        allow_paid_stars: int | None
        suggested_post: TLObject | None
        def __init__(self, *, silent: bool = ..., background: bool = ..., clear_draft: bool = ..., noforwards: bool = ..., update_stickersets_order: bool = ..., invert_media: bool = ..., allow_paid_floodskip: bool = ..., peer: TLObject, reply_to: TLObject | None = ..., media: TLObject, message: str, random_id: int, reply_markup: TLObject | None = ..., entities: list[TLObject] | None = ..., schedule_date: int | None = ..., schedule_repeat_period: int | None = ..., send_as: TLObject | None = ..., quick_reply_shortcut: TLObject | None = ..., effect: int | None = ..., allow_paid_stars: int | None = ..., suggested_post: TLObject | None = ...) -> None: ...

    class sendMessage(TLObject):
        no_webpage: bool
        silent: bool
        background: bool
        clear_draft: bool
        noforwards: bool
        update_stickersets_order: bool
        invert_media: bool
        allow_paid_floodskip: bool
        peer: TLObject
        reply_to: TLObject | None
        message: str
        random_id: int
        reply_markup: TLObject | None
        entities: list[TLObject] | None
        schedule_date: int | None
        schedule_repeat_period: int | None
        send_as: TLObject | None
        quick_reply_shortcut: TLObject | None
        effect: int | None
        allow_paid_stars: int | None
        suggested_post: TLObject | None
        rich_message: TLObject | None
        def __init__(self, *, no_webpage: bool = ..., silent: bool = ..., background: bool = ..., clear_draft: bool = ..., noforwards: bool = ..., update_stickersets_order: bool = ..., invert_media: bool = ..., allow_paid_floodskip: bool = ..., peer: TLObject, reply_to: TLObject | None = ..., message: str, random_id: int, reply_markup: TLObject | None = ..., entities: list[TLObject] | None = ..., schedule_date: int | None = ..., schedule_repeat_period: int | None = ..., send_as: TLObject | None = ..., quick_reply_shortcut: TLObject | None = ..., effect: int | None = ..., allow_paid_stars: int | None = ..., suggested_post: TLObject | None = ..., rich_message: TLObject | None = ...) -> None: ...

    class sendMultiMedia(TLObject):
        silent: bool
        background: bool
        clear_draft: bool
        noforwards: bool
        update_stickersets_order: bool
        invert_media: bool
        allow_paid_floodskip: bool
        peer: TLObject
        reply_to: TLObject | None
        multi_media: list[TLObject]
        schedule_date: int | None
        send_as: TLObject | None
        quick_reply_shortcut: TLObject | None
        effect: int | None
        allow_paid_stars: int | None
        def __init__(self, *, silent: bool = ..., background: bool = ..., clear_draft: bool = ..., noforwards: bool = ..., update_stickersets_order: bool = ..., invert_media: bool = ..., allow_paid_floodskip: bool = ..., peer: TLObject, reply_to: TLObject | None = ..., multi_media: list[TLObject], schedule_date: int | None = ..., send_as: TLObject | None = ..., quick_reply_shortcut: TLObject | None = ..., effect: int | None = ..., allow_paid_stars: int | None = ...) -> None: ...

    class sendPaidReaction(TLObject):
        peer: TLObject
        msg_id: int
        count: int
        random_id: int
        private: TLObject | None
        def __init__(self, *, peer: TLObject, msg_id: int, count: int, random_id: int, private: TLObject | None = ...) -> None: ...

    class sendQuickReplyMessages(TLObject):
        peer: TLObject
        shortcut_id: int
        id: list[int]
        random_id: list[int]
        def __init__(self, *, peer: TLObject, shortcut_id: int, id: list[int], random_id: list[int]) -> None: ...

    class sendReaction(TLObject):
        big: bool
        add_to_recent: bool
        peer: TLObject
        msg_id: int
        reaction: list[TLObject] | None
        def __init__(self, *, big: bool = ..., add_to_recent: bool = ..., peer: TLObject, msg_id: int, reaction: list[TLObject] | None = ...) -> None: ...

    class sendScheduledMessages(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class sendScreenshotNotification(TLObject):
        peer: TLObject
        reply_to: TLObject
        random_id: int
        def __init__(self, *, peer: TLObject, reply_to: TLObject, random_id: int) -> None: ...

    class sendVote(TLObject):
        peer: TLObject
        msg_id: int
        options: list[bytes]
        def __init__(self, *, peer: TLObject, msg_id: int, options: list[bytes]) -> None: ...

    class sendWebViewData(TLObject):
        bot: TLObject
        random_id: int
        button_text: str
        data: str
        def __init__(self, *, bot: TLObject, random_id: int, button_text: str, data: str) -> None: ...

    class sendWebViewResultMessage(TLObject):
        bot_query_id: str
        result: TLObject
        def __init__(self, *, bot_query_id: str, result: TLObject) -> None: ...

    class sentEncryptedFile(TLObject):
        date: int
        file: TLObject
        def __init__(self, *, date: int, file: TLObject) -> None: ...

    class sentEncryptedMessage(TLObject):
        date: int
        def __init__(self, *, date: int) -> None: ...

    class setBotCallbackAnswer(TLObject):
        alert: bool
        query_id: int
        message: str | None
        url: str | None
        cache_time: int
        def __init__(self, *, alert: bool = ..., query_id: int, message: str | None = ..., url: str | None = ..., cache_time: int) -> None: ...

    class setBotGuestChatResult(TLObject):
        query_id: int
        result: TLObject
        def __init__(self, *, query_id: int, result: TLObject) -> None: ...

    class setBotPrecheckoutResults(TLObject):
        success: bool
        query_id: int
        error: str | None
        def __init__(self, *, success: bool = ..., query_id: int, error: str | None = ...) -> None: ...

    class setBotShippingResults(TLObject):
        query_id: int
        error: str | None
        shipping_options: list[TLObject] | None
        def __init__(self, *, query_id: int, error: str | None = ..., shipping_options: list[TLObject] | None = ...) -> None: ...

    class setBotWidgetQueryAnswer(TLObject):
        query_id: int
        result: str | None
        def __init__(self, *, query_id: int, result: str | None = ...) -> None: ...

    class setChatAvailableReactions(TLObject):
        peer: TLObject
        available_reactions: TLObject
        reactions_limit: int | None
        paid_enabled: bool
        def __init__(self, *, peer: TLObject, available_reactions: TLObject, reactions_limit: int | None = ..., paid_enabled: bool = ...) -> None: ...

    class setChatTheme(TLObject):
        peer: TLObject
        theme: TLObject
        def __init__(self, *, peer: TLObject, theme: TLObject) -> None: ...

    class setChatWallPaper(TLObject):
        for_both: bool
        revert: bool
        peer: TLObject
        wallpaper: TLObject | None
        settings: TLObject | None
        id: int | None
        def __init__(self, *, for_both: bool = ..., revert: bool = ..., peer: TLObject, wallpaper: TLObject | None = ..., settings: TLObject | None = ..., id: int | None = ...) -> None: ...

    class setDefaultHistoryTTL(TLObject):
        period: int
        def __init__(self, *, period: int) -> None: ...

    class setDefaultReaction(TLObject):
        reaction: TLObject
        def __init__(self, *, reaction: TLObject) -> None: ...

    class setEncryptedTyping(TLObject):
        peer: TLObject
        typing: bool
        def __init__(self, *, peer: TLObject, typing: bool) -> None: ...

    class setGameScore(TLObject):
        edit_message: bool
        force: bool
        peer: TLObject
        id: int
        user_id: TLObject
        score: int
        def __init__(self, *, edit_message: bool = ..., force: bool = ..., peer: TLObject, id: int, user_id: TLObject, score: int) -> None: ...

    class setHistoryTTL(TLObject):
        peer: TLObject
        period: int
        def __init__(self, *, peer: TLObject, period: int) -> None: ...

    class setInlineBotResults(TLObject):
        gallery: bool
        private: bool
        query_id: int
        results: list[TLObject]
        cache_time: int
        next_offset: str | None
        switch_pm: TLObject | None
        switch_webview: TLObject | None
        def __init__(self, *, gallery: bool = ..., private: bool = ..., query_id: int, results: list[TLObject], cache_time: int, next_offset: str | None = ..., switch_pm: TLObject | None = ..., switch_webview: TLObject | None = ...) -> None: ...

    class setInlineGameScore(TLObject):
        edit_message: bool
        force: bool
        id: TLObject
        user_id: TLObject
        score: int
        def __init__(self, *, edit_message: bool = ..., force: bool = ..., id: TLObject, user_id: TLObject, score: int) -> None: ...

    class setShareTheme(TLObject):
        peer: TLObject
        theme: TLObject
        def __init__(self, *, peer: TLObject, theme: TLObject) -> None: ...

    class setTyping(TLObject):
        peer: TLObject
        top_msg_id: int | None
        action: TLObject
        def __init__(self, *, peer: TLObject, top_msg_id: int | None = ..., action: TLObject) -> None: ...

    class sponsoredMessages(TLObject):
        posts_between: int | None
        start_delay: int | None
        between_delay: int | None
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, posts_between: int | None = ..., start_delay: int | None = ..., between_delay: int | None = ..., messages: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class sponsoredMessagesEmpty(TLObject):
        def __init__(self) -> None: ...

    class startBot(TLObject):
        bot: TLObject
        peer: TLObject
        random_id: int
        start_param: str
        def __init__(self, *, bot: TLObject, peer: TLObject, random_id: int, start_param: str) -> None: ...

    class startHistoryImport(TLObject):
        peer: TLObject
        import_id: int
        def __init__(self, *, peer: TLObject, import_id: int) -> None: ...

    class stickerSet(TLObject):
        set: TLObject
        packs: list[TLObject]
        keywords: list[TLObject]
        documents: list[TLObject]
        def __init__(self, *, set: TLObject, packs: list[TLObject], keywords: list[TLObject], documents: list[TLObject]) -> None: ...

    class stickerSetInstallResultArchive(TLObject):
        sets: list[TLObject]
        def __init__(self, *, sets: list[TLObject]) -> None: ...

    class stickerSetInstallResultSuccess(TLObject):
        def __init__(self) -> None: ...

    class stickerSetNotModified(TLObject):
        def __init__(self) -> None: ...

    class stickers(TLObject):
        hash: int
        stickers: list[TLObject]
        def __init__(self, *, hash: int, stickers: list[TLObject]) -> None: ...

    class stickersNotModified(TLObject):
        def __init__(self) -> None: ...

    class summarizeText(TLObject):
        peer: TLObject
        id: int
        to_lang: str | None
        tone: str | None
        def __init__(self, *, peer: TLObject, id: int, to_lang: str | None = ..., tone: str | None = ...) -> None: ...

    class toggleBotInAttachMenu(TLObject):
        write_allowed: bool
        bot: TLObject
        enabled: bool
        def __init__(self, *, write_allowed: bool = ..., bot: TLObject, enabled: bool) -> None: ...

    class toggleDialogFilterTags(TLObject):
        enabled: bool
        def __init__(self, *, enabled: bool) -> None: ...

    class toggleDialogPin(TLObject):
        pinned: bool
        peer: TLObject
        def __init__(self, *, pinned: bool = ..., peer: TLObject) -> None: ...

    class toggleNoForwards(TLObject):
        peer: TLObject
        enabled: bool
        request_msg_id: int | None
        def __init__(self, *, peer: TLObject, enabled: bool, request_msg_id: int | None = ...) -> None: ...

    class togglePaidReactionPrivacy(TLObject):
        peer: TLObject
        msg_id: int
        private: TLObject
        def __init__(self, *, peer: TLObject, msg_id: int, private: TLObject) -> None: ...

    class togglePeerTranslations(TLObject):
        disabled: bool
        peer: TLObject
        def __init__(self, *, disabled: bool = ..., peer: TLObject) -> None: ...

    class toggleSavedDialogPin(TLObject):
        pinned: bool
        peer: TLObject
        def __init__(self, *, pinned: bool = ..., peer: TLObject) -> None: ...

    class toggleStickerSets(TLObject):
        uninstall: bool
        archive: bool
        unarchive: bool
        stickersets: list[TLObject]
        def __init__(self, *, uninstall: bool = ..., archive: bool = ..., unarchive: bool = ..., stickersets: list[TLObject]) -> None: ...

    class toggleSuggestedPostApproval(TLObject):
        reject: bool
        peer: TLObject
        msg_id: int
        schedule_date: int | None
        reject_comment: str | None
        def __init__(self, *, reject: bool = ..., peer: TLObject, msg_id: int, schedule_date: int | None = ..., reject_comment: str | None = ...) -> None: ...

    class toggleTodoCompleted(TLObject):
        peer: TLObject
        msg_id: int
        completed: list[int]
        incompleted: list[int]
        def __init__(self, *, peer: TLObject, msg_id: int, completed: list[int], incompleted: list[int]) -> None: ...

    class transcribeAudio(TLObject):
        peer: TLObject
        msg_id: int
        def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

    class transcribeAudioFile(TLObject):
        file: TLObject
        def __init__(self, *, file: TLObject) -> None: ...

    class transcribedAudio(TLObject):
        pending: bool
        transcription_id: int
        text: str
        trial_remains_num: int | None
        trial_remains_until_date: int | None
        def __init__(self, *, pending: bool = ..., transcription_id: int, text: str, trial_remains_num: int | None = ..., trial_remains_until_date: int | None = ...) -> None: ...

    class translateResult(TLObject):
        result: list[TLObject]
        def __init__(self, *, result: list[TLObject]) -> None: ...

    class translateRichMessage(TLObject):
        peer: TLObject | None
        id: list[int] | None
        text: list[TLObject] | None
        to_lang: str
        tone: str | None
        def __init__(self, *, peer: TLObject | None = ..., id: list[int] | None = ..., text: list[TLObject] | None = ..., to_lang: str, tone: str | None = ...) -> None: ...

    class translateText(TLObject):
        peer: TLObject | None
        id: list[int] | None
        text: list[TLObject] | None
        to_lang: str
        tone: str | None
        def __init__(self, *, peer: TLObject | None = ..., id: list[int] | None = ..., text: list[TLObject] | None = ..., to_lang: str, tone: str | None = ...) -> None: ...

    class translatedRichMessage(TLObject):
        result: list[TLObject]
        def __init__(self, *, result: list[TLObject]) -> None: ...

    class uninstallStickerSet(TLObject):
        stickerset: TLObject
        def __init__(self, *, stickerset: TLObject) -> None: ...

    class unpinAllMessages(TLObject):
        peer: TLObject
        top_msg_id: int | None
        saved_peer_id: TLObject | None
        def __init__(self, *, peer: TLObject, top_msg_id: int | None = ..., saved_peer_id: TLObject | None = ...) -> None: ...

    class updateDialogFilter(TLObject):
        id: int
        filter: TLObject | None
        def __init__(self, *, id: int, filter: TLObject | None = ...) -> None: ...

    class updateDialogFiltersOrder(TLObject):
        order: list[int]
        def __init__(self, *, order: list[int]) -> None: ...

    class updatePinnedForumTopic(TLObject):
        peer: TLObject
        topic_id: int
        pinned: bool
        def __init__(self, *, peer: TLObject, topic_id: int, pinned: bool) -> None: ...

    class updatePinnedMessage(TLObject):
        silent: bool
        unpin: bool
        pm_oneside: bool
        peer: TLObject
        id: int
        def __init__(self, *, silent: bool = ..., unpin: bool = ..., pm_oneside: bool = ..., peer: TLObject, id: int) -> None: ...

    class updateSavedReactionTag(TLObject):
        reaction: TLObject
        title: str | None
        def __init__(self, *, reaction: TLObject, title: str | None = ...) -> None: ...

    class uploadEncryptedFile(TLObject):
        peer: TLObject
        file: TLObject
        def __init__(self, *, peer: TLObject, file: TLObject) -> None: ...

    class uploadImportedMedia(TLObject):
        peer: TLObject
        import_id: int
        file_name: str
        media: TLObject
        def __init__(self, *, peer: TLObject, import_id: int, file_name: str, media: TLObject) -> None: ...

    class uploadMedia(TLObject):
        business_connection_id: str | None
        peer: TLObject
        media: TLObject
        def __init__(self, *, business_connection_id: str | None = ..., peer: TLObject, media: TLObject) -> None: ...

    class viewSponsoredMessage(TLObject):
        random_id: bytes
        def __init__(self, *, random_id: bytes) -> None: ...

    class votesList(TLObject):
        count: int
        votes: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        next_offset: str | None
        def __init__(self, *, count: int, votes: list[TLObject], chats: list[TLObject], users: list[TLObject], next_offset: str | None = ...) -> None: ...

    class webPage(TLObject):
        webpage: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, webpage: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class webPagePreview(TLObject):
        media: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, media: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class widgetPublicData(TLObject):
        hash: int
        data: str
        period: int
        def __init__(self, *, hash: int, data: str, period: int) -> None: ...

    class widgetPublicDataNotModified(TLObject):
        period: int
        def __init__(self, *, period: int) -> None: ...

class missingInvitee(TLObject):
    premium_would_allow_invite: bool
    premium_required_for_pm: bool
    user_id: int
    def __init__(self, *, premium_would_allow_invite: bool = ..., premium_required_for_pm: bool = ..., user_id: int) -> None: ...

class monoForumDialog(TLObject):
    unread_mark: bool
    nopaid_messages_exception: bool
    peer: TLObject
    top_message: int
    read_inbox_max_id: int
    read_outbox_max_id: int
    unread_count: int
    unread_reactions_count: int
    draft: TLObject | None
    def __init__(self, *, unread_mark: bool = ..., nopaid_messages_exception: bool = ..., peer: TLObject, top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_reactions_count: int, draft: TLObject | None = ...) -> None: ...

class myBoost(TLObject):
    slot: int
    peer: TLObject | None
    date: int
    expires: int
    cooldown_until_date: int | None
    def __init__(self, *, slot: int, peer: TLObject | None = ..., date: int, expires: int, cooldown_until_date: int | None = ...) -> None: ...

class nearestDc(TLObject):
    country: str
    this_dc: int
    nearest_dc: int
    def __init__(self, *, country: str, this_dc: int, nearest_dc: int) -> None: ...

class notificationSoundDefault(TLObject):
    def __init__(self) -> None: ...

class notificationSoundLocal(TLObject):
    title: str
    data: str
    def __init__(self, *, title: str, data: str) -> None: ...

class notificationSoundNone(TLObject):
    def __init__(self) -> None: ...

class notificationSoundRingtone(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class notifyBroadcasts(TLObject):
    def __init__(self) -> None: ...

class notifyChats(TLObject):
    def __init__(self) -> None: ...

class notifyCommunity(TLObject):
    community_id: int
    def __init__(self, *, community_id: int) -> None: ...

class notifyForumTopic(TLObject):
    peer: TLObject
    top_msg_id: int
    def __init__(self, *, peer: TLObject, top_msg_id: int) -> None: ...

class notifyPeer(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class notifyUsers(TLObject):
    def __init__(self) -> None: ...

class null(TLObject):
    def __init__(self) -> None: ...

class onrampAvailability(TLObject):
    allowed: bool
    buy_allowed: bool
    country_code: str
    state: str | None
    methods: list[TLObject]
    def __init__(self, *, allowed: bool = ..., buy_allowed: bool = ..., country_code: str, state: str | None = ..., methods: list[TLObject]) -> None: ...

class onrampLimits(TLObject):
    base_currency: str
    base_min_amount: str
    base_max_amount: str
    crypto_min_amount: str
    crypto_max_amount: str
    payment_method: str
    def __init__(self, *, base_currency: str, base_min_amount: str, base_max_amount: str, crypto_min_amount: str, crypto_max_amount: str, payment_method: str) -> None: ...

class onrampMethodAvailability(TLObject):
    available: bool
    payment_method: str
    def __init__(self, *, available: bool = ..., payment_method: str) -> None: ...

class onrampProviderInfo(TLObject):
    supports_base_currencies: bool
    supports_limits: bool
    supports_quote: bool
    id: str
    name: str
    crypto_currencies: list[str]
    def __init__(self, *, supports_base_currencies: bool = ..., supports_limits: bool = ..., supports_quote: bool = ..., id: str, name: str, crypto_currencies: list[str]) -> None: ...

class onrampQuote(TLObject):
    base_currency: str
    base_amount: str
    crypto_currency: str
    crypto_amount: str
    crypto_price: str
    fee_amount: str
    extra_fee_amount: str
    network_fee_amount: str
    total_amount: str
    payment_method: str
    expires_date: int
    def __init__(self, *, base_currency: str, base_amount: str, crypto_currency: str, crypto_amount: str, crypto_price: str, fee_amount: str, extra_fee_amount: str, network_fee_amount: str, total_amount: str, payment_method: str, expires_date: int) -> None: ...

class onrampSession(TLObject):
    provider: str
    session_id: str
    url: str
    expires_date: int
    def __init__(self, *, provider: str, session_id: str, url: str, expires_date: int) -> None: ...

class outboxReadDate(TLObject):
    date: int
    def __init__(self, *, date: int) -> None: ...

class page(TLObject):
    part: bool
    rtl: bool
    v2: bool
    url: str
    blocks: list[TLObject]
    photos: list[TLObject]
    documents: list[TLObject]
    views: int | None
    def __init__(self, *, part: bool = ..., rtl: bool = ..., v2: bool = ..., url: str, blocks: list[TLObject], photos: list[TLObject], documents: list[TLObject], views: int | None = ...) -> None: ...

class pageBlockAnchor(TLObject):
    name: str
    def __init__(self, *, name: str) -> None: ...

class pageBlockAudio(TLObject):
    audio_id: int
    caption: TLObject
    def __init__(self, *, audio_id: int, caption: TLObject) -> None: ...

class pageBlockAuthorDate(TLObject):
    author: TLObject
    published_date: int
    def __init__(self, *, author: TLObject, published_date: int) -> None: ...

class pageBlockBlockquote(TLObject):
    collapsed: bool
    text: TLObject
    caption: TLObject
    def __init__(self, *, collapsed: bool = ..., text: TLObject, caption: TLObject) -> None: ...

class pageBlockBlockquoteBlocks(TLObject):
    blocks: list[TLObject]
    caption: TLObject
    def __init__(self, *, blocks: list[TLObject], caption: TLObject) -> None: ...

class pageBlockButtonRow(TLObject):
    align_left: bool
    align_center: bool
    align_right: bool
    buttons: list[TLObject]
    def __init__(self, *, align_left: bool = ..., align_center: bool = ..., align_right: bool = ..., buttons: list[TLObject]) -> None: ...

class pageBlockChannel(TLObject):
    channel: TLObject
    def __init__(self, *, channel: TLObject) -> None: ...

class pageBlockCollage(TLObject):
    items: list[TLObject]
    caption: TLObject
    def __init__(self, *, items: list[TLObject], caption: TLObject) -> None: ...

class pageBlockCover(TLObject):
    cover: TLObject
    def __init__(self, *, cover: TLObject) -> None: ...

class pageBlockDetails(TLObject):
    open: bool
    blocks: list[TLObject]
    title: TLObject
    def __init__(self, *, open: bool = ..., blocks: list[TLObject], title: TLObject) -> None: ...

class pageBlockDivider(TLObject):
    def __init__(self) -> None: ...

class pageBlockDocument(TLObject):
    document_id: int
    caption: TLObject
    def __init__(self, *, document_id: int, caption: TLObject) -> None: ...

class pageBlockEmbed(TLObject):
    full_width: bool
    allow_scrolling: bool
    url: str | None
    html: str | None
    poster_photo_id: int | None
    w: int | None
    h: int | None
    caption: TLObject
    def __init__(self, *, full_width: bool = ..., allow_scrolling: bool = ..., url: str | None = ..., html: str | None = ..., poster_photo_id: int | None = ..., w: int | None = ..., h: int | None = ..., caption: TLObject) -> None: ...

class pageBlockEmbedPost(TLObject):
    url: str
    webpage_id: int
    author_photo_id: int
    author: str
    date: int
    blocks: list[TLObject]
    caption: TLObject
    def __init__(self, *, url: str, webpage_id: int, author_photo_id: int, author: str, date: int, blocks: list[TLObject], caption: TLObject) -> None: ...

class pageBlockFooter(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockHeader(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockHeading1(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockHeading2(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockHeading3(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockHeading4(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockHeading5(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockHeading6(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockKicker(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockList(TLObject):
    items: list[TLObject]
    def __init__(self, *, items: list[TLObject]) -> None: ...

class pageBlockMap(TLObject):
    geo: TLObject
    zoom: int
    w: int
    h: int
    caption: TLObject
    def __init__(self, *, geo: TLObject, zoom: int, w: int, h: int, caption: TLObject) -> None: ...

class pageBlockMath(TLObject):
    source: str
    def __init__(self, *, source: str) -> None: ...

class pageBlockOrderedList(TLObject):
    reversed: bool
    items: list[TLObject]
    start: int | None
    type: str | None
    def __init__(self, *, reversed: bool = ..., items: list[TLObject], start: int | None = ..., type: str | None = ...) -> None: ...

class pageBlockParagraph(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockPhoto(TLObject):
    spoiler: bool
    photo_id: int
    caption: TLObject
    url: str | None
    webpage_id: int | None
    def __init__(self, *, spoiler: bool = ..., photo_id: int, caption: TLObject, url: str | None = ..., webpage_id: int | None = ...) -> None: ...

class pageBlockPreformatted(TLObject):
    text: TLObject
    language: str
    def __init__(self, *, text: TLObject, language: str) -> None: ...

class pageBlockPullquote(TLObject):
    text: TLObject
    caption: TLObject
    def __init__(self, *, text: TLObject, caption: TLObject) -> None: ...

class pageBlockRelatedArticles(TLObject):
    title: TLObject
    articles: list[TLObject]
    def __init__(self, *, title: TLObject, articles: list[TLObject]) -> None: ...

class pageBlockSlideshow(TLObject):
    items: list[TLObject]
    caption: TLObject
    def __init__(self, *, items: list[TLObject], caption: TLObject) -> None: ...

class pageBlockSubheader(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockSubtitle(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockTable(TLObject):
    bordered: bool
    striped: bool
    compact: bool
    title: TLObject
    rows: list[TLObject]
    def __init__(self, *, bordered: bool = ..., striped: bool = ..., compact: bool = ..., title: TLObject, rows: list[TLObject]) -> None: ...

class pageBlockThinking(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockTitle(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class pageBlockUnsupported(TLObject):
    def __init__(self) -> None: ...

class pageBlockVideo(TLObject):
    autoplay: bool
    loop: bool
    spoiler: bool
    video_id: int
    caption: TLObject
    def __init__(self, *, autoplay: bool = ..., loop: bool = ..., spoiler: bool = ..., video_id: int, caption: TLObject) -> None: ...

class pageButton(TLObject):
    text: TLObject
    type: TLObject
    style: TLObject | None
    def __init__(self, *, text: TLObject, type: TLObject, style: TLObject | None = ...) -> None: ...

class pageCaption(TLObject):
    text: TLObject
    credit: TLObject
    def __init__(self, *, text: TLObject, credit: TLObject) -> None: ...

class pageListItemBlocks(TLObject):
    checkbox: bool
    checked: bool
    blocks: list[TLObject]
    def __init__(self, *, checkbox: bool = ..., checked: bool = ..., blocks: list[TLObject]) -> None: ...

class pageListItemText(TLObject):
    checkbox: bool
    checked: bool
    text: TLObject
    def __init__(self, *, checkbox: bool = ..., checked: bool = ..., text: TLObject) -> None: ...

class pageListOrderedItemBlocks(TLObject):
    checkbox: bool
    checked: bool
    num: str | None
    blocks: list[TLObject]
    value: int | None
    type: str | None
    def __init__(self, *, checkbox: bool = ..., checked: bool = ..., num: str | None = ..., blocks: list[TLObject], value: int | None = ..., type: str | None = ...) -> None: ...

class pageListOrderedItemText(TLObject):
    checkbox: bool
    checked: bool
    num: str | None
    text: TLObject
    value: int | None
    type: str | None
    def __init__(self, *, checkbox: bool = ..., checked: bool = ..., num: str | None = ..., text: TLObject, value: int | None = ..., type: str | None = ...) -> None: ...

class pageRelatedArticle(TLObject):
    url: str
    webpage_id: int
    title: str | None
    description: str | None
    photo_id: int | None
    author: str | None
    published_date: int | None
    def __init__(self, *, url: str, webpage_id: int, title: str | None = ..., description: str | None = ..., photo_id: int | None = ..., author: str | None = ..., published_date: int | None = ...) -> None: ...

class pageTableCell(TLObject):
    header: bool
    align_center: bool
    align_right: bool
    valign_middle: bool
    valign_bottom: bool
    text: TLObject | None
    colspan: int | None
    rowspan: int | None
    def __init__(self, *, header: bool = ..., align_center: bool = ..., align_right: bool = ..., valign_middle: bool = ..., valign_bottom: bool = ..., text: TLObject | None = ..., colspan: int | None = ..., rowspan: int | None = ...) -> None: ...

class pageTableRow(TLObject):
    cells: list[TLObject]
    def __init__(self, *, cells: list[TLObject]) -> None: ...

class paidReactionPrivacyAnonymous(TLObject):
    def __init__(self) -> None: ...

class paidReactionPrivacyDefault(TLObject):
    def __init__(self) -> None: ...

class paidReactionPrivacyPeer(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class passkey(TLObject):
    id: str
    name: str
    date: int
    software_emoji_id: int | None
    last_usage_date: int | None
    def __init__(self, *, id: str, name: str, date: int, software_emoji_id: int | None = ..., last_usage_date: int | None = ...) -> None: ...

class passwordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow(TLObject):
    salt1: bytes
    salt2: bytes
    g: int
    p: bytes
    def __init__(self, *, salt1: bytes, salt2: bytes, g: int, p: bytes) -> None: ...

class passwordKdfAlgoUnknown(TLObject):
    def __init__(self) -> None: ...

class paymentCharge(TLObject):
    id: str
    provider_charge_id: str
    def __init__(self, *, id: str, provider_charge_id: str) -> None: ...

class paymentFormMethod(TLObject):
    url: str
    title: str
    def __init__(self, *, url: str, title: str) -> None: ...

class paymentRequestedInfo(TLObject):
    name: str | None
    phone: str | None
    email: str | None
    shipping_address: TLObject | None
    def __init__(self, *, name: str | None = ..., phone: str | None = ..., email: str | None = ..., shipping_address: TLObject | None = ...) -> None: ...

class paymentSavedCredentialsCard(TLObject):
    id: str
    title: str
    def __init__(self, *, id: str, title: str) -> None: ...

class payments:
    class applyGiftCode(TLObject):
        slug: str
        def __init__(self, *, slug: str) -> None: ...

    class assignAppStoreTransaction(TLObject):
        receipt: bytes
        purpose: TLObject
        def __init__(self, *, receipt: bytes, purpose: TLObject) -> None: ...

    class assignPlayMarketTransaction(TLObject):
        receipt: TLObject
        purpose: TLObject
        def __init__(self, *, receipt: TLObject, purpose: TLObject) -> None: ...

    class bankCardData(TLObject):
        title: str
        open_urls: list[TLObject]
        def __init__(self, *, title: str, open_urls: list[TLObject]) -> None: ...

    class botCancelStarsSubscription(TLObject):
        restore: bool
        user_id: TLObject
        charge_id: str
        def __init__(self, *, restore: bool = ..., user_id: TLObject, charge_id: str) -> None: ...

    class canPurchaseStore(TLObject):
        purpose: TLObject
        def __init__(self, *, purpose: TLObject) -> None: ...

    class changeStarsSubscription(TLObject):
        peer: TLObject
        subscription_id: str
        canceled: bool
        def __init__(self, *, peer: TLObject, subscription_id: str, canceled: bool = ...) -> None: ...

    class checkCanSendGift(TLObject):
        gift_id: int
        def __init__(self, *, gift_id: int) -> None: ...

    class checkCanSendGiftResultFail(TLObject):
        reason: TLObject
        def __init__(self, *, reason: TLObject) -> None: ...

    class checkCanSendGiftResultOk(TLObject):
        def __init__(self) -> None: ...

    class checkGiftCode(TLObject):
        slug: str
        def __init__(self, *, slug: str) -> None: ...

    class checkedGiftCode(TLObject):
        via_giveaway: bool
        from_id: TLObject | None
        giveaway_msg_id: int | None
        to_id: int | None
        date: int
        days: int
        used_date: int | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, via_giveaway: bool = ..., from_id: TLObject | None = ..., giveaway_msg_id: int | None = ..., to_id: int | None = ..., date: int, days: int, used_date: int | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class clearSavedInfo(TLObject):
        credentials: bool
        info: bool
        def __init__(self, *, credentials: bool = ..., info: bool = ...) -> None: ...

    class connectStarRefBot(TLObject):
        peer: TLObject
        bot: TLObject
        def __init__(self, *, peer: TLObject, bot: TLObject) -> None: ...

    class connectedStarRefBots(TLObject):
        count: int
        connected_bots: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, connected_bots: list[TLObject], users: list[TLObject]) -> None: ...

    class convertStarGift(TLObject):
        stargift: TLObject
        def __init__(self, *, stargift: TLObject) -> None: ...

    class craftStarGift(TLObject):
        stargift: list[TLObject]
        def __init__(self, *, stargift: list[TLObject]) -> None: ...

    class createOnrampSession(TLObject):
        provider: str
        crypto_currency: str
        address: str
        payment_method: str | None
        base_currency: str | None
        base_amount: str | None
        memo: str | None
        theme: str | None
        success_return_url: str | None
        fail_return_url: str | None
        crypto_amount: str | None
        def __init__(self, *, provider: str, crypto_currency: str, address: str, payment_method: str | None = ..., base_currency: str | None = ..., base_amount: str | None = ..., memo: str | None = ..., theme: str | None = ..., success_return_url: str | None = ..., fail_return_url: str | None = ..., crypto_amount: str | None = ...) -> None: ...

    class createStarGiftCollection(TLObject):
        peer: TLObject
        title: str
        stargift: list[TLObject]
        def __init__(self, *, peer: TLObject, title: str, stargift: list[TLObject]) -> None: ...

    class currencyRates(TLObject):
        rates: list[TLObject]
        def __init__(self, *, rates: list[TLObject]) -> None: ...

    class deleteStarGift(TLObject):
        stargift: TLObject
        def __init__(self, *, stargift: TLObject) -> None: ...

    class deleteStarGiftCollection(TLObject):
        peer: TLObject
        collection_id: int
        def __init__(self, *, peer: TLObject, collection_id: int) -> None: ...

    class depositStarGift(TLObject):
        hide_sender: bool
        peer: TLObject
        slug: str
        def __init__(self, *, hide_sender: bool = ..., peer: TLObject, slug: str) -> None: ...

    class displayStarGift(TLObject):
        peer: TLObject | None
        slug: str
        def __init__(self, *, peer: TLObject | None = ..., slug: str) -> None: ...

    class editConnectedStarRefBot(TLObject):
        revoked: bool
        peer: TLObject
        link: str
        def __init__(self, *, revoked: bool = ..., peer: TLObject, link: str) -> None: ...

    class exportInvoice(TLObject):
        invoice_media: TLObject
        def __init__(self, *, invoice_media: TLObject) -> None: ...

    class exportedInvoice(TLObject):
        url: str
        def __init__(self, *, url: str) -> None: ...

    class fulfillStarsSubscription(TLObject):
        peer: TLObject
        subscription_id: str
        def __init__(self, *, peer: TLObject, subscription_id: str) -> None: ...

    class getBankCardData(TLObject):
        number: str
        def __init__(self, *, number: str) -> None: ...

    class getConnectedStarRefBot(TLObject):
        peer: TLObject
        bot: TLObject
        def __init__(self, *, peer: TLObject, bot: TLObject) -> None: ...

    class getConnectedStarRefBots(TLObject):
        peer: TLObject
        offset_date: int | None
        offset_link: str | None
        limit: int
        def __init__(self, *, peer: TLObject, offset_date: int | None = ..., offset_link: str | None = ..., limit: int) -> None: ...

    class getCraftStarGifts(TLObject):
        gift_id: int
        offset: str
        limit: int
        def __init__(self, *, gift_id: int, offset: str, limit: int) -> None: ...

    class getCurrencyRates(TLObject):
        def __init__(self) -> None: ...

    class getGiveawayInfo(TLObject):
        peer: TLObject
        msg_id: int
        def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

    class getOnrampAvailability(TLObject):
        provider: str
        crypto_currency: str
        base_currency: str | None
        def __init__(self, *, provider: str, crypto_currency: str, base_currency: str | None = ...) -> None: ...

    class getOnrampBaseCurrencies(TLObject):
        provider: str
        crypto_currency: str
        def __init__(self, *, provider: str, crypto_currency: str) -> None: ...

    class getOnrampLimits(TLObject):
        provider: str
        crypto_currency: str
        base_currency: str
        payment_method: str | None
        def __init__(self, *, provider: str, crypto_currency: str, base_currency: str, payment_method: str | None = ...) -> None: ...

    class getOnrampProviders(TLObject):
        crypto_currency: str | None
        def __init__(self, *, crypto_currency: str | None = ...) -> None: ...

    class getOnrampQuote(TLObject):
        provider: str
        crypto_currency: str
        base_currency: str
        base_amount: str | None
        crypto_amount: str | None
        payment_method: str | None
        def __init__(self, *, provider: str, crypto_currency: str, base_currency: str, base_amount: str | None = ..., crypto_amount: str | None = ..., payment_method: str | None = ...) -> None: ...

    class getPaymentForm(TLObject):
        invoice: TLObject
        theme_params: TLObject | None
        def __init__(self, *, invoice: TLObject, theme_params: TLObject | None = ...) -> None: ...

    class getPaymentReceipt(TLObject):
        peer: TLObject
        msg_id: int
        def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

    class getPremiumGiftCodeOptions(TLObject):
        boost_peer: TLObject | None
        def __init__(self, *, boost_peer: TLObject | None = ...) -> None: ...

    class getResaleStarGifts(TLObject):
        sort_by_price: bool
        sort_by_num: bool
        for_craft: bool
        stars_only: bool
        attributes_hash: int | None
        gift_id: int
        attributes: list[TLObject] | None
        offset: str
        limit: int
        def __init__(self, *, sort_by_price: bool = ..., sort_by_num: bool = ..., for_craft: bool = ..., stars_only: bool = ..., attributes_hash: int | None = ..., gift_id: int, attributes: list[TLObject] | None = ..., offset: str, limit: int) -> None: ...

    class getSavedInfo(TLObject):
        def __init__(self) -> None: ...

    class getSavedStarGift(TLObject):
        stargift: list[TLObject]
        def __init__(self, *, stargift: list[TLObject]) -> None: ...

    class getSavedStarGifts(TLObject):
        exclude_unsaved: bool
        exclude_saved: bool
        exclude_unlimited: bool
        exclude_unique: bool
        sort_by_value: bool
        exclude_upgradable: bool
        exclude_unupgradable: bool
        peer_color_available: bool
        exclude_hosted: bool
        peer: TLObject
        collection_id: int | None
        offset: str
        limit: int
        def __init__(self, *, exclude_unsaved: bool = ..., exclude_saved: bool = ..., exclude_unlimited: bool = ..., exclude_unique: bool = ..., sort_by_value: bool = ..., exclude_upgradable: bool = ..., exclude_unupgradable: bool = ..., peer_color_available: bool = ..., exclude_hosted: bool = ..., peer: TLObject, collection_id: int | None = ..., offset: str, limit: int) -> None: ...

    class getStarGiftActiveAuctions(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getStarGiftAuctionAcquiredGifts(TLObject):
        gift_id: int
        def __init__(self, *, gift_id: int) -> None: ...

    class getStarGiftAuctionState(TLObject):
        auction: TLObject
        version: int
        def __init__(self, *, auction: TLObject, version: int) -> None: ...

    class getStarGiftCollections(TLObject):
        peer: TLObject
        hash: int
        def __init__(self, *, peer: TLObject, hash: int) -> None: ...

    class getStarGiftUpgradeAttributes(TLObject):
        gift_id: int
        def __init__(self, *, gift_id: int) -> None: ...

    class getStarGiftUpgradePreview(TLObject):
        gift_id: int
        def __init__(self, *, gift_id: int) -> None: ...

    class getStarGiftWithdrawalUrl(TLObject):
        stargift: TLObject
        tmp_password: bytes
        def __init__(self, *, stargift: TLObject, tmp_password: bytes) -> None: ...

    class getStarGifts(TLObject):
        hash: int
        def __init__(self, *, hash: int) -> None: ...

    class getStarsGiftOptions(TLObject):
        user_id: TLObject | None
        def __init__(self, *, user_id: TLObject | None = ...) -> None: ...

    class getStarsGiveawayOptions(TLObject):
        def __init__(self) -> None: ...

    class getStarsRevenueAdsAccountUrl(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getStarsRevenueStats(TLObject):
        dark: bool
        ton: bool
        peer: TLObject
        def __init__(self, *, dark: bool = ..., ton: bool = ..., peer: TLObject) -> None: ...

    class getStarsRevenueWithdrawalUrl(TLObject):
        ton: bool
        peer: TLObject
        amount: int | None
        password: TLObject
        def __init__(self, *, ton: bool = ..., peer: TLObject, amount: int | None = ..., password: TLObject) -> None: ...

    class getStarsStatus(TLObject):
        ton: bool
        peer: TLObject
        def __init__(self, *, ton: bool = ..., peer: TLObject) -> None: ...

    class getStarsSubscriptions(TLObject):
        missing_balance: bool
        peer: TLObject
        offset: str
        def __init__(self, *, missing_balance: bool = ..., peer: TLObject, offset: str) -> None: ...

    class getStarsTopupOptions(TLObject):
        def __init__(self) -> None: ...

    class getStarsTransactions(TLObject):
        inbound: bool
        outbound: bool
        ascending: bool
        ton: bool
        subscription_id: str | None
        peer: TLObject
        offset: str
        limit: int
        def __init__(self, *, inbound: bool = ..., outbound: bool = ..., ascending: bool = ..., ton: bool = ..., subscription_id: str | None = ..., peer: TLObject, offset: str, limit: int) -> None: ...

    class getStarsTransactionsByID(TLObject):
        ton: bool
        peer: TLObject
        id: list[TLObject]
        def __init__(self, *, ton: bool = ..., peer: TLObject, id: list[TLObject]) -> None: ...

    class getSuggestedStarRefBots(TLObject):
        order_by_revenue: bool
        order_by_date: bool
        peer: TLObject
        offset: str
        limit: int
        def __init__(self, *, order_by_revenue: bool = ..., order_by_date: bool = ..., peer: TLObject, offset: str, limit: int) -> None: ...

    class getUniqueStarGift(TLObject):
        slug: str
        def __init__(self, *, slug: str) -> None: ...

    class getUniqueStarGiftValueInfo(TLObject):
        slug: str
        def __init__(self, *, slug: str) -> None: ...

    class giveawayInfo(TLObject):
        participating: bool
        preparing_results: bool
        start_date: int
        joined_too_early_date: int | None
        admin_disallowed_chat_id: int | None
        disallowed_country: str | None
        def __init__(self, *, participating: bool = ..., preparing_results: bool = ..., start_date: int, joined_too_early_date: int | None = ..., admin_disallowed_chat_id: int | None = ..., disallowed_country: str | None = ...) -> None: ...

    class giveawayInfoResults(TLObject):
        winner: bool
        refunded: bool
        start_date: int
        gift_code_slug: str | None
        stars_prize: int | None
        finish_date: int
        winners_count: int
        activated_count: int | None
        def __init__(self, *, winner: bool = ..., refunded: bool = ..., start_date: int, gift_code_slug: str | None = ..., stars_prize: int | None = ..., finish_date: int, winners_count: int, activated_count: int | None = ...) -> None: ...

    class launchPrepaidGiveaway(TLObject):
        peer: TLObject
        giveaway_id: int
        purpose: TLObject
        def __init__(self, *, peer: TLObject, giveaway_id: int, purpose: TLObject) -> None: ...

    class paymentForm(TLObject):
        can_save_credentials: bool
        password_missing: bool
        form_id: int
        bot_id: int
        title: str
        description: str
        photo: TLObject | None
        invoice: TLObject
        provider_id: int
        url: str
        native_provider: str | None
        native_params: TLObject | None
        additional_methods: list[TLObject] | None
        saved_info: TLObject | None
        saved_credentials: list[TLObject] | None
        users: list[TLObject]
        def __init__(self, *, can_save_credentials: bool = ..., password_missing: bool = ..., form_id: int, bot_id: int, title: str, description: str, photo: TLObject | None = ..., invoice: TLObject, provider_id: int, url: str, native_provider: str | None = ..., native_params: TLObject | None = ..., additional_methods: list[TLObject] | None = ..., saved_info: TLObject | None = ..., saved_credentials: list[TLObject] | None = ..., users: list[TLObject]) -> None: ...

    class paymentFormStarGift(TLObject):
        form_id: int
        invoice: TLObject
        def __init__(self, *, form_id: int, invoice: TLObject) -> None: ...

    class paymentFormStars(TLObject):
        form_id: int
        bot_id: int
        title: str
        description: str
        photo: TLObject | None
        invoice: TLObject
        users: list[TLObject]
        def __init__(self, *, form_id: int, bot_id: int, title: str, description: str, photo: TLObject | None = ..., invoice: TLObject, users: list[TLObject]) -> None: ...

    class paymentReceipt(TLObject):
        date: int
        bot_id: int
        provider_id: int
        title: str
        description: str
        photo: TLObject | None
        invoice: TLObject
        info: TLObject | None
        shipping: TLObject | None
        tip_amount: int | None
        currency: str
        total_amount: int
        credentials_title: str
        users: list[TLObject]
        def __init__(self, *, date: int, bot_id: int, provider_id: int, title: str, description: str, photo: TLObject | None = ..., invoice: TLObject, info: TLObject | None = ..., shipping: TLObject | None = ..., tip_amount: int | None = ..., currency: str, total_amount: int, credentials_title: str, users: list[TLObject]) -> None: ...

    class paymentReceiptStars(TLObject):
        date: int
        bot_id: int
        title: str
        description: str
        photo: TLObject | None
        invoice: TLObject
        currency: str
        total_amount: int
        transaction_id: str
        users: list[TLObject]
        def __init__(self, *, date: int, bot_id: int, title: str, description: str, photo: TLObject | None = ..., invoice: TLObject, currency: str, total_amount: int, transaction_id: str, users: list[TLObject]) -> None: ...

    class paymentResult(TLObject):
        updates: TLObject
        def __init__(self, *, updates: TLObject) -> None: ...

    class paymentVerificationNeeded(TLObject):
        url: str
        def __init__(self, *, url: str) -> None: ...

    class refundStarsCharge(TLObject):
        user_id: TLObject
        charge_id: str
        def __init__(self, *, user_id: TLObject, charge_id: str) -> None: ...

    class reorderStarGiftCollections(TLObject):
        peer: TLObject
        order: list[int]
        def __init__(self, *, peer: TLObject, order: list[int]) -> None: ...

    class resaleStarGifts(TLObject):
        count: int
        gifts: list[TLObject]
        next_offset: str | None
        attributes: list[TLObject] | None
        attributes_hash: int | None
        chats: list[TLObject]
        counters: list[TLObject] | None
        users: list[TLObject]
        def __init__(self, *, count: int, gifts: list[TLObject], next_offset: str | None = ..., attributes: list[TLObject] | None = ..., attributes_hash: int | None = ..., chats: list[TLObject], counters: list[TLObject] | None = ..., users: list[TLObject]) -> None: ...

    class resolveStarGiftOffer(TLObject):
        decline: bool
        offer_msg_id: int
        def __init__(self, *, decline: bool = ..., offer_msg_id: int) -> None: ...

    class saveStarGift(TLObject):
        unsave: bool
        stargift: TLObject
        def __init__(self, *, unsave: bool = ..., stargift: TLObject) -> None: ...

    class savedInfo(TLObject):
        has_saved_credentials: bool
        saved_info: TLObject | None
        def __init__(self, *, has_saved_credentials: bool = ..., saved_info: TLObject | None = ...) -> None: ...

    class savedStarGifts(TLObject):
        count: int
        chat_notifications_enabled: bool
        gifts: list[TLObject]
        next_offset: str | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, chat_notifications_enabled: bool = ..., gifts: list[TLObject], next_offset: str | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class sendPaymentForm(TLObject):
        form_id: int
        invoice: TLObject
        requested_info_id: str | None
        shipping_option_id: str | None
        credentials: TLObject
        tip_amount: int | None
        def __init__(self, *, form_id: int, invoice: TLObject, requested_info_id: str | None = ..., shipping_option_id: str | None = ..., credentials: TLObject, tip_amount: int | None = ...) -> None: ...

    class sendStarGiftOffer(TLObject):
        peer: TLObject
        slug: str
        price: TLObject
        duration: int
        random_id: int
        allow_paid_stars: int | None
        def __init__(self, *, peer: TLObject, slug: str, price: TLObject, duration: int, random_id: int, allow_paid_stars: int | None = ...) -> None: ...

    class sendStarsForm(TLObject):
        form_id: int
        invoice: TLObject
        def __init__(self, *, form_id: int, invoice: TLObject) -> None: ...

    class starGiftActiveAuctions(TLObject):
        auctions: list[TLObject]
        users: list[TLObject]
        chats: list[TLObject]
        def __init__(self, *, auctions: list[TLObject], users: list[TLObject], chats: list[TLObject]) -> None: ...

    class starGiftActiveAuctionsNotModified(TLObject):
        def __init__(self) -> None: ...

    class starGiftAuctionAcquiredGifts(TLObject):
        gifts: list[TLObject]
        users: list[TLObject]
        chats: list[TLObject]
        def __init__(self, *, gifts: list[TLObject], users: list[TLObject], chats: list[TLObject]) -> None: ...

    class starGiftAuctionState(TLObject):
        gift: TLObject
        state: TLObject
        user_state: TLObject
        timeout: int
        users: list[TLObject]
        chats: list[TLObject]
        def __init__(self, *, gift: TLObject, state: TLObject, user_state: TLObject, timeout: int, users: list[TLObject], chats: list[TLObject]) -> None: ...

    class starGiftCollections(TLObject):
        collections: list[TLObject]
        def __init__(self, *, collections: list[TLObject]) -> None: ...

    class starGiftCollectionsNotModified(TLObject):
        def __init__(self) -> None: ...

    class starGiftDepositPayload(TLObject):
        nft_address: str
        payload: bytes
        amount: int
        def __init__(self, *, nft_address: str, payload: bytes, amount: int) -> None: ...

    class starGiftUpgradeAttributes(TLObject):
        attributes: list[TLObject]
        def __init__(self, *, attributes: list[TLObject]) -> None: ...

    class starGiftUpgradePreview(TLObject):
        sample_attributes: list[TLObject]
        prices: list[TLObject]
        next_prices: list[TLObject]
        def __init__(self, *, sample_attributes: list[TLObject], prices: list[TLObject], next_prices: list[TLObject]) -> None: ...

    class starGiftWithdrawalUrl(TLObject):
        url: str
        def __init__(self, *, url: str) -> None: ...

    class starGifts(TLObject):
        hash: int
        gifts: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, hash: int, gifts: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class starGiftsNotModified(TLObject):
        def __init__(self) -> None: ...

    class starsRevenueAdsAccountUrl(TLObject):
        url: str
        def __init__(self, *, url: str) -> None: ...

    class starsRevenueStats(TLObject):
        top_hours_graph: TLObject | None
        revenue_graph: TLObject
        status: TLObject
        usd_rate: float
        def __init__(self, *, top_hours_graph: TLObject | None = ..., revenue_graph: TLObject, status: TLObject, usd_rate: float) -> None: ...

    class starsRevenueWithdrawalUrl(TLObject):
        url: str
        def __init__(self, *, url: str) -> None: ...

    class starsStatus(TLObject):
        balance: TLObject
        subscriptions: list[TLObject] | None
        subscriptions_next_offset: str | None
        subscriptions_missing_balance: int | None
        history: list[TLObject] | None
        next_offset: str | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, balance: TLObject, subscriptions: list[TLObject] | None = ..., subscriptions_next_offset: str | None = ..., subscriptions_missing_balance: int | None = ..., history: list[TLObject] | None = ..., next_offset: str | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class suggestedStarRefBots(TLObject):
        count: int
        suggested_bots: list[TLObject]
        users: list[TLObject]
        next_offset: str | None
        def __init__(self, *, count: int, suggested_bots: list[TLObject], users: list[TLObject], next_offset: str | None = ...) -> None: ...

    class toggleChatStarGiftNotifications(TLObject):
        enabled: bool
        peer: TLObject
        def __init__(self, *, enabled: bool = ..., peer: TLObject) -> None: ...

    class toggleStarGiftsPinnedToTop(TLObject):
        peer: TLObject
        stargift: list[TLObject]
        def __init__(self, *, peer: TLObject, stargift: list[TLObject]) -> None: ...

    class transferStarGift(TLObject):
        stargift: TLObject
        to_id: TLObject
        def __init__(self, *, stargift: TLObject, to_id: TLObject) -> None: ...

    class uniqueStarGift(TLObject):
        gift: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, gift: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class uniqueStarGiftValueInfo(TLObject):
        last_sale_on_fragment: bool
        value_is_average: bool
        currency: str
        value: int
        initial_sale_date: int
        initial_sale_stars: int
        initial_sale_price: int
        last_sale_date: int | None
        last_sale_price: int | None
        floor_price: int | None
        average_price: int | None
        listed_count: int | None
        fragment_listed_count: int | None
        fragment_listed_url: str | None
        def __init__(self, *, last_sale_on_fragment: bool = ..., value_is_average: bool = ..., currency: str, value: int, initial_sale_date: int, initial_sale_stars: int, initial_sale_price: int, last_sale_date: int | None = ..., last_sale_price: int | None = ..., floor_price: int | None = ..., average_price: int | None = ..., listed_count: int | None = ..., fragment_listed_count: int | None = ..., fragment_listed_url: str | None = ...) -> None: ...

    class updateStarGiftCollection(TLObject):
        peer: TLObject
        collection_id: int
        title: str | None
        delete_stargift: list[TLObject] | None
        add_stargift: list[TLObject] | None
        order: list[TLObject] | None
        def __init__(self, *, peer: TLObject, collection_id: int, title: str | None = ..., delete_stargift: list[TLObject] | None = ..., add_stargift: list[TLObject] | None = ..., order: list[TLObject] | None = ...) -> None: ...

    class updateStarGiftPrice(TLObject):
        stargift: TLObject
        resell_amount: TLObject
        def __init__(self, *, stargift: TLObject, resell_amount: TLObject) -> None: ...

    class upgradeStarGift(TLObject):
        keep_original_details: bool
        stargift: TLObject
        def __init__(self, *, keep_original_details: bool = ..., stargift: TLObject) -> None: ...

    class validateRequestedInfo(TLObject):
        save: bool
        invoice: TLObject
        info: TLObject
        def __init__(self, *, save: bool = ..., invoice: TLObject, info: TLObject) -> None: ...

    class validatedRequestedInfo(TLObject):
        id: str | None
        shipping_options: list[TLObject] | None
        def __init__(self, *, id: str | None = ..., shipping_options: list[TLObject] | None = ...) -> None: ...

    class withdrawStarGift(TLObject):
        keep_on_profile: bool
        stargift: TLObject
        tmp_password: bytes
        def __init__(self, *, keep_on_profile: bool = ..., stargift: TLObject, tmp_password: bytes) -> None: ...

class peerBlocked(TLObject):
    peer_id: TLObject
    date: int
    def __init__(self, *, peer_id: TLObject, date: int) -> None: ...

class peerChannel(TLObject):
    channel_id: int
    def __init__(self, *, channel_id: int) -> None: ...

class peerChat(TLObject):
    chat_id: int
    def __init__(self, *, chat_id: int) -> None: ...

class peerColor(TLObject):
    color: int | None
    background_emoji_id: int | None
    def __init__(self, *, color: int | None = ..., background_emoji_id: int | None = ...) -> None: ...

class peerColorCollectible(TLObject):
    collectible_id: int
    gift_emoji_id: int
    background_emoji_id: int
    accent_color: int
    colors: list[int]
    dark_accent_color: int | None
    dark_colors: list[int] | None
    def __init__(self, *, collectible_id: int, gift_emoji_id: int, background_emoji_id: int, accent_color: int, colors: list[int], dark_accent_color: int | None = ..., dark_colors: list[int] | None = ...) -> None: ...

class peerLocated(TLObject):
    peer: TLObject
    expires: int
    distance: int
    def __init__(self, *, peer: TLObject, expires: int, distance: int) -> None: ...

class peerNotifySettings(TLObject):
    show_previews: bool
    silent: bool
    mute_until: int | None
    ios_sound: TLObject | None
    android_sound: TLObject | None
    other_sound: TLObject | None
    stories_muted: bool
    stories_hide_sender: bool
    stories_ios_sound: TLObject | None
    stories_android_sound: TLObject | None
    stories_other_sound: TLObject | None
    def __init__(self, *, show_previews: bool = ..., silent: bool = ..., mute_until: int | None = ..., ios_sound: TLObject | None = ..., android_sound: TLObject | None = ..., other_sound: TLObject | None = ..., stories_muted: bool = ..., stories_hide_sender: bool = ..., stories_ios_sound: TLObject | None = ..., stories_android_sound: TLObject | None = ..., stories_other_sound: TLObject | None = ...) -> None: ...

class peerSelfLocated(TLObject):
    expires: int
    def __init__(self, *, expires: int) -> None: ...

class peerSettings(TLObject):
    report_spam: bool
    add_contact: bool
    block_contact: bool
    share_contact: bool
    need_contacts_exception: bool
    report_geo: bool
    autoarchived: bool
    invite_members: bool
    request_chat_broadcast: bool
    business_bot_paused: bool
    business_bot_can_reply: bool
    geo_distance: int | None
    request_chat_title: str | None
    request_chat_date: int | None
    business_bot_id: int | None
    business_bot_manage_url: str | None
    charge_paid_message_stars: int | None
    registration_month: str | None
    phone_country: str | None
    name_change_date: int | None
    photo_change_date: int | None
    def __init__(self, *, report_spam: bool = ..., add_contact: bool = ..., block_contact: bool = ..., share_contact: bool = ..., need_contacts_exception: bool = ..., report_geo: bool = ..., autoarchived: bool = ..., invite_members: bool = ..., request_chat_broadcast: bool = ..., business_bot_paused: bool = ..., business_bot_can_reply: bool = ..., geo_distance: int | None = ..., request_chat_title: str | None = ..., request_chat_date: int | None = ..., business_bot_id: int | None = ..., business_bot_manage_url: str | None = ..., charge_paid_message_stars: int | None = ..., registration_month: str | None = ..., phone_country: str | None = ..., name_change_date: int | None = ..., photo_change_date: int | None = ...) -> None: ...

class peerStories(TLObject):
    peer: TLObject
    max_read_id: int | None
    stories: list[TLObject]
    def __init__(self, *, peer: TLObject, max_read_id: int | None = ..., stories: list[TLObject]) -> None: ...

class peerUser(TLObject):
    user_id: int
    def __init__(self, *, user_id: int) -> None: ...

class pendingSuggestion(TLObject):
    suggestion: str
    title: TLObject
    description: TLObject
    url: str
    def __init__(self, *, suggestion: str, title: TLObject, description: TLObject, url: str) -> None: ...

class phone:
    class acceptCall(TLObject):
        peer: TLObject
        g_b: bytes
        protocol: TLObject
        def __init__(self, *, peer: TLObject, g_b: bytes, protocol: TLObject) -> None: ...

    class checkGroupCall(TLObject):
        call: TLObject
        sources: list[int]
        def __init__(self, *, call: TLObject, sources: list[int]) -> None: ...

    class confirmCall(TLObject):
        peer: TLObject
        g_a: bytes
        key_fingerprint: int
        protocol: TLObject
        def __init__(self, *, peer: TLObject, g_a: bytes, key_fingerprint: int, protocol: TLObject) -> None: ...

    class createConferenceCall(TLObject):
        muted: bool
        video_stopped: bool
        join: bool
        random_id: int
        public_key: int | bytes | None
        block: bytes | None
        params: TLObject | None
        def __init__(self, *, muted: bool = ..., video_stopped: bool = ..., join: bool = ..., random_id: int, public_key: int | bytes | None = ..., block: bytes | None = ..., params: TLObject | None = ...) -> None: ...

    class createGroupCall(TLObject):
        rtmp_stream: bool
        peer: TLObject
        random_id: int
        title: str | None
        schedule_date: int | None
        def __init__(self, *, rtmp_stream: bool = ..., peer: TLObject, random_id: int, title: str | None = ..., schedule_date: int | None = ...) -> None: ...

    class declineConferenceCallInvite(TLObject):
        msg_id: int
        def __init__(self, *, msg_id: int) -> None: ...

    class deleteConferenceCallParticipants(TLObject):
        only_left: bool
        kick: bool
        call: TLObject
        ids: list[int]
        block: bytes
        def __init__(self, *, only_left: bool = ..., kick: bool = ..., call: TLObject, ids: list[int], block: bytes) -> None: ...

    class deleteGroupCallMessages(TLObject):
        report_spam: bool
        call: TLObject
        messages: list[int]
        def __init__(self, *, report_spam: bool = ..., call: TLObject, messages: list[int]) -> None: ...

    class deleteGroupCallParticipantMessages(TLObject):
        report_spam: bool
        call: TLObject
        participant: TLObject
        def __init__(self, *, report_spam: bool = ..., call: TLObject, participant: TLObject) -> None: ...

    class discardCall(TLObject):
        video: bool
        peer: TLObject
        duration: int
        reason: TLObject
        connection_id: int
        def __init__(self, *, video: bool = ..., peer: TLObject, duration: int, reason: TLObject, connection_id: int) -> None: ...

    class discardGroupCall(TLObject):
        call: TLObject
        def __init__(self, *, call: TLObject) -> None: ...

    class editGroupCallParticipant(TLObject):
        call: TLObject
        participant: TLObject
        muted: bool
        volume: int | None
        raise_hand: bool
        video_stopped: bool
        video_paused: bool
        presentation_paused: bool
        def __init__(self, *, call: TLObject, participant: TLObject, muted: bool = ..., volume: int | None = ..., raise_hand: bool = ..., video_stopped: bool = ..., video_paused: bool = ..., presentation_paused: bool = ...) -> None: ...

    class editGroupCallTitle(TLObject):
        call: TLObject
        title: str
        def __init__(self, *, call: TLObject, title: str) -> None: ...

    class exportGroupCallInvite(TLObject):
        can_self_unmute: bool
        call: TLObject
        def __init__(self, *, can_self_unmute: bool = ..., call: TLObject) -> None: ...

    class exportedGroupCallInvite(TLObject):
        link: str
        def __init__(self, *, link: str) -> None: ...

    class getCallConfig(TLObject):
        def __init__(self) -> None: ...

    class getGroupCall(TLObject):
        call: TLObject
        limit: int
        def __init__(self, *, call: TLObject, limit: int) -> None: ...

    class getGroupCallChainBlocks(TLObject):
        call: TLObject
        sub_chain_id: int
        offset: int
        limit: int
        def __init__(self, *, call: TLObject, sub_chain_id: int, offset: int, limit: int) -> None: ...

    class getGroupCallJoinAs(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getGroupCallStars(TLObject):
        call: TLObject
        def __init__(self, *, call: TLObject) -> None: ...

    class getGroupCallStreamChannels(TLObject):
        call: TLObject
        def __init__(self, *, call: TLObject) -> None: ...

    class getGroupCallStreamRtmpUrl(TLObject):
        live_story: bool
        peer: TLObject
        revoke: bool
        def __init__(self, *, live_story: bool = ..., peer: TLObject, revoke: bool) -> None: ...

    class getGroupParticipants(TLObject):
        call: TLObject
        ids: list[TLObject]
        sources: list[int]
        offset: str
        limit: int
        def __init__(self, *, call: TLObject, ids: list[TLObject], sources: list[int], offset: str, limit: int) -> None: ...

    class groupCall(TLObject):
        call: TLObject
        participants: list[TLObject]
        participants_next_offset: str
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, call: TLObject, participants: list[TLObject], participants_next_offset: str, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class groupCallStars(TLObject):
        total_stars: int
        top_donors: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, total_stars: int, top_donors: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class groupCallStreamChannels(TLObject):
        channels: list[TLObject]
        def __init__(self, *, channels: list[TLObject]) -> None: ...

    class groupCallStreamRtmpUrl(TLObject):
        url: str
        key: str
        def __init__(self, *, url: str, key: str) -> None: ...

    class groupParticipants(TLObject):
        count: int
        participants: list[TLObject]
        next_offset: str
        chats: list[TLObject]
        users: list[TLObject]
        version: int
        def __init__(self, *, count: int, participants: list[TLObject], next_offset: str, chats: list[TLObject], users: list[TLObject], version: int) -> None: ...

    class inviteConferenceCallParticipant(TLObject):
        video: bool
        call: TLObject
        user_id: TLObject
        def __init__(self, *, video: bool = ..., call: TLObject, user_id: TLObject) -> None: ...

    class inviteToGroupCall(TLObject):
        call: TLObject
        users: list[TLObject]
        def __init__(self, *, call: TLObject, users: list[TLObject]) -> None: ...

    class joinAsPeers(TLObject):
        peers: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, peers: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class joinGroupCall(TLObject):
        muted: bool
        video_stopped: bool
        call: TLObject
        join_as: TLObject
        invite_hash: str | None
        public_key: int | bytes | None
        block: bytes | None
        params: TLObject
        def __init__(self, *, muted: bool = ..., video_stopped: bool = ..., call: TLObject, join_as: TLObject, invite_hash: str | None = ..., public_key: int | bytes | None = ..., block: bytes | None = ..., params: TLObject) -> None: ...

    class joinGroupCallPresentation(TLObject):
        call: TLObject
        params: TLObject
        def __init__(self, *, call: TLObject, params: TLObject) -> None: ...

    class leaveGroupCall(TLObject):
        call: TLObject
        source: int
        def __init__(self, *, call: TLObject, source: int) -> None: ...

    class leaveGroupCallPresentation(TLObject):
        call: TLObject
        def __init__(self, *, call: TLObject) -> None: ...

    class phoneCall(TLObject):
        phone_call: TLObject
        users: list[TLObject]
        def __init__(self, *, phone_call: TLObject, users: list[TLObject]) -> None: ...

    class receivedCall(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class requestCall(TLObject):
        video: bool
        user_id: TLObject
        random_id: int
        g_a_hash: bytes
        protocol: TLObject
        def __init__(self, *, video: bool = ..., user_id: TLObject, random_id: int, g_a_hash: bytes, protocol: TLObject) -> None: ...

    class saveCallDebug(TLObject):
        peer: TLObject
        debug: TLObject
        def __init__(self, *, peer: TLObject, debug: TLObject) -> None: ...

    class saveCallLog(TLObject):
        peer: TLObject
        file: TLObject
        def __init__(self, *, peer: TLObject, file: TLObject) -> None: ...

    class saveDefaultGroupCallJoinAs(TLObject):
        peer: TLObject
        join_as: TLObject
        def __init__(self, *, peer: TLObject, join_as: TLObject) -> None: ...

    class saveDefaultSendAs(TLObject):
        call: TLObject
        send_as: TLObject
        def __init__(self, *, call: TLObject, send_as: TLObject) -> None: ...

    class sendConferenceCallBroadcast(TLObject):
        call: TLObject
        block: bytes
        def __init__(self, *, call: TLObject, block: bytes) -> None: ...

    class sendGroupCallEncryptedMessage(TLObject):
        call: TLObject
        encrypted_message: bytes
        def __init__(self, *, call: TLObject, encrypted_message: bytes) -> None: ...

    class sendGroupCallMessage(TLObject):
        call: TLObject
        random_id: int
        message: TLObject
        allow_paid_stars: int | None
        send_as: TLObject | None
        def __init__(self, *, call: TLObject, random_id: int, message: TLObject, allow_paid_stars: int | None = ..., send_as: TLObject | None = ...) -> None: ...

    class sendSignalingData(TLObject):
        peer: TLObject
        data: bytes
        def __init__(self, *, peer: TLObject, data: bytes) -> None: ...

    class setCallRating(TLObject):
        user_initiative: bool
        peer: TLObject
        rating: int
        comment: str
        def __init__(self, *, user_initiative: bool = ..., peer: TLObject, rating: int, comment: str) -> None: ...

    class startScheduledGroupCall(TLObject):
        call: TLObject
        def __init__(self, *, call: TLObject) -> None: ...

    class toggleGroupCallRecord(TLObject):
        start: bool
        video: bool
        call: TLObject
        title: str | None
        video_portrait: bool
        def __init__(self, *, start: bool = ..., video: bool = ..., call: TLObject, title: str | None = ..., video_portrait: bool = ...) -> None: ...

    class toggleGroupCallSettings(TLObject):
        reset_invite_hash: bool
        call: TLObject
        join_muted: bool
        messages_enabled: bool
        send_paid_messages_stars: int | None
        def __init__(self, *, reset_invite_hash: bool = ..., call: TLObject, join_muted: bool = ..., messages_enabled: bool = ..., send_paid_messages_stars: int | None = ...) -> None: ...

    class toggleGroupCallStartSubscription(TLObject):
        call: TLObject
        subscribed: bool
        def __init__(self, *, call: TLObject, subscribed: bool) -> None: ...

class phoneCall(TLObject):
    p2p_allowed: bool
    video: bool
    conference_supported: bool
    id: int
    access_hash: int
    date: int
    admin_id: int
    participant_id: int
    g_a_or_b: bytes
    key_fingerprint: int
    protocol: TLObject
    connections: list[TLObject]
    start_date: int
    custom_parameters: TLObject | None
    def __init__(self, *, p2p_allowed: bool = ..., video: bool = ..., conference_supported: bool = ..., id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_or_b: bytes, key_fingerprint: int, protocol: TLObject, connections: list[TLObject], start_date: int, custom_parameters: TLObject | None = ...) -> None: ...

class phoneCallAccepted(TLObject):
    video: bool
    id: int
    access_hash: int
    date: int
    admin_id: int
    participant_id: int
    g_b: bytes
    protocol: TLObject
    def __init__(self, *, video: bool = ..., id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_b: bytes, protocol: TLObject) -> None: ...

class phoneCallDiscardReasonBusy(TLObject):
    def __init__(self) -> None: ...

class phoneCallDiscardReasonDisconnect(TLObject):
    def __init__(self) -> None: ...

class phoneCallDiscardReasonHangup(TLObject):
    def __init__(self) -> None: ...

class phoneCallDiscardReasonMigrateConferenceCall(TLObject):
    slug: str
    def __init__(self, *, slug: str) -> None: ...

class phoneCallDiscardReasonMissed(TLObject):
    def __init__(self) -> None: ...

class phoneCallDiscarded(TLObject):
    need_rating: bool
    need_debug: bool
    video: bool
    id: int
    reason: TLObject | None
    duration: int | None
    def __init__(self, *, need_rating: bool = ..., need_debug: bool = ..., video: bool = ..., id: int, reason: TLObject | None = ..., duration: int | None = ...) -> None: ...

class phoneCallEmpty(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class phoneCallProtocol(TLObject):
    udp_p2p: bool
    udp_reflector: bool
    min_layer: int
    max_layer: int
    library_versions: list[str]
    def __init__(self, *, udp_p2p: bool = ..., udp_reflector: bool = ..., min_layer: int, max_layer: int, library_versions: list[str]) -> None: ...

class phoneCallRequested(TLObject):
    video: bool
    id: int
    access_hash: int
    date: int
    admin_id: int
    participant_id: int
    g_a_hash: bytes
    protocol: TLObject
    def __init__(self, *, video: bool = ..., id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_hash: bytes, protocol: TLObject) -> None: ...

class phoneCallWaiting(TLObject):
    video: bool
    id: int
    access_hash: int
    date: int
    admin_id: int
    participant_id: int
    protocol: TLObject
    receive_date: int | None
    def __init__(self, *, video: bool = ..., id: int, access_hash: int, date: int, admin_id: int, participant_id: int, protocol: TLObject, receive_date: int | None = ...) -> None: ...

class phoneConnection(TLObject):
    tcp: bool
    id: int
    ip: str
    ipv6: str
    port: int
    peer_tag: bytes
    def __init__(self, *, tcp: bool = ..., id: int, ip: str, ipv6: str, port: int, peer_tag: bytes) -> None: ...

class phoneConnectionWebrtc(TLObject):
    turn: bool
    stun: bool
    id: int
    ip: str
    ipv6: str
    port: int
    username: str
    password: str
    def __init__(self, *, turn: bool = ..., stun: bool = ..., id: int, ip: str, ipv6: str, port: int, username: str, password: str) -> None: ...

class photo(TLObject):
    has_stickers: bool
    id: int
    access_hash: int
    file_reference: bytes
    date: int
    sizes: list[TLObject]
    video_sizes: list[TLObject] | None
    dc_id: int
    def __init__(self, *, has_stickers: bool = ..., id: int, access_hash: int, file_reference: bytes, date: int, sizes: list[TLObject], video_sizes: list[TLObject] | None = ..., dc_id: int) -> None: ...

class photoCachedSize(TLObject):
    type: str
    w: int
    h: int
    bytes: bytes
    def __init__(self, *, type: str, w: int, h: int, bytes: bytes) -> None: ...

class photoEmpty(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class photoPathSize(TLObject):
    type: str
    bytes: bytes
    def __init__(self, *, type: str, bytes: bytes) -> None: ...

class photoSize(TLObject):
    type: str
    w: int
    h: int
    size: int
    def __init__(self, *, type: str, w: int, h: int, size: int) -> None: ...

class photoSizeEmpty(TLObject):
    type: str
    def __init__(self, *, type: str) -> None: ...

class photoSizeProgressive(TLObject):
    type: str
    w: int
    h: int
    sizes: list[int]
    def __init__(self, *, type: str, w: int, h: int, sizes: list[int]) -> None: ...

class photoStrippedSize(TLObject):
    type: str
    bytes: bytes
    def __init__(self, *, type: str, bytes: bytes) -> None: ...

class photos:
    class deletePhotos(TLObject):
        id: list[TLObject]
        def __init__(self, *, id: list[TLObject]) -> None: ...

    class getUserPhotos(TLObject):
        user_id: TLObject
        offset: int
        max_id: int
        limit: int
        def __init__(self, *, user_id: TLObject, offset: int, max_id: int, limit: int) -> None: ...

    class photo(TLObject):
        photo: TLObject
        users: list[TLObject]
        def __init__(self, *, photo: TLObject, users: list[TLObject]) -> None: ...

    class photos(TLObject):
        photos: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, photos: list[TLObject], users: list[TLObject]) -> None: ...

    class photosSlice(TLObject):
        count: int
        photos: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, photos: list[TLObject], users: list[TLObject]) -> None: ...

    class updateProfilePhoto(TLObject):
        fallback: bool
        bot: TLObject | None
        id: TLObject
        def __init__(self, *, fallback: bool = ..., bot: TLObject | None = ..., id: TLObject) -> None: ...

    class uploadContactProfilePhoto(TLObject):
        suggest: bool
        save: bool
        user_id: TLObject
        file: TLObject | None
        video: TLObject | None
        video_start_ts: float | None
        video_emoji_markup: TLObject | None
        def __init__(self, *, suggest: bool = ..., save: bool = ..., user_id: TLObject, file: TLObject | None = ..., video: TLObject | None = ..., video_start_ts: float | None = ..., video_emoji_markup: TLObject | None = ...) -> None: ...

    class uploadProfilePhoto(TLObject):
        fallback: bool
        bot: TLObject | None
        file: TLObject | None
        video: TLObject | None
        video_start_ts: float | None
        video_emoji_markup: TLObject | None
        def __init__(self, *, fallback: bool = ..., bot: TLObject | None = ..., file: TLObject | None = ..., video: TLObject | None = ..., video_start_ts: float | None = ..., video_emoji_markup: TLObject | None = ...) -> None: ...

class poll(TLObject):
    id: int
    closed: bool
    public_voters: bool
    multiple_choice: bool
    quiz: bool
    open_answers: bool
    revoting_disabled: bool
    shuffle_answers: bool
    hide_results_until_close: bool
    creator: bool
    subscribers_only: bool
    question: TLObject
    answers: list[TLObject]
    close_period: int | None
    close_date: int | None
    countries_iso2: list[str] | None
    hash: int
    def __init__(self, *, id: int, closed: bool = ..., public_voters: bool = ..., multiple_choice: bool = ..., quiz: bool = ..., open_answers: bool = ..., revoting_disabled: bool = ..., shuffle_answers: bool = ..., hide_results_until_close: bool = ..., creator: bool = ..., subscribers_only: bool = ..., question: TLObject, answers: list[TLObject], close_period: int | None = ..., close_date: int | None = ..., countries_iso2: list[str] | None = ..., hash: int) -> None: ...

class pollAnswer(TLObject):
    text: TLObject
    option: bytes
    media: TLObject | None
    added_by: TLObject | None
    date: int | None
    def __init__(self, *, text: TLObject, option: bytes, media: TLObject | None = ..., added_by: TLObject | None = ..., date: int | None = ...) -> None: ...

class pollAnswerVoters(TLObject):
    chosen: bool
    correct: bool
    option: bytes
    voters: int | None
    recent_voters: list[TLObject] | None
    def __init__(self, *, chosen: bool = ..., correct: bool = ..., option: bytes, voters: int | None = ..., recent_voters: list[TLObject] | None = ...) -> None: ...

class pollResults(TLObject):
    min: bool
    has_unread_votes: bool
    can_view_stats: bool
    results: list[TLObject] | None
    total_voters: int | None
    recent_voters: list[TLObject] | None
    solution: str | None
    solution_entities: list[TLObject] | None
    solution_media: TLObject | None
    def __init__(self, *, min: bool = ..., has_unread_votes: bool = ..., can_view_stats: bool = ..., results: list[TLObject] | None = ..., total_voters: int | None = ..., recent_voters: list[TLObject] | None = ..., solution: str | None = ..., solution_entities: list[TLObject] | None = ..., solution_media: TLObject | None = ...) -> None: ...

class popularContact(TLObject):
    client_id: int
    importers: int
    def __init__(self, *, client_id: int, importers: int) -> None: ...

class postAddress(TLObject):
    street_line1: str
    street_line2: str
    city: str
    state: str
    country_iso2: str
    post_code: str
    def __init__(self, *, street_line1: str, street_line2: str, city: str, state: str, country_iso2: str, post_code: str) -> None: ...

class postInteractionCountersMessage(TLObject):
    msg_id: int
    views: int
    forwards: int
    reactions: int
    def __init__(self, *, msg_id: int, views: int, forwards: int, reactions: int) -> None: ...

class postInteractionCountersStory(TLObject):
    story_id: int
    views: int
    forwards: int
    reactions: int
    def __init__(self, *, story_id: int, views: int, forwards: int, reactions: int) -> None: ...

class premium:
    class applyBoost(TLObject):
        slots: list[int] | None
        peer: TLObject
        def __init__(self, *, slots: list[int] | None = ..., peer: TLObject) -> None: ...

    class boostsList(TLObject):
        count: int
        boosts: list[TLObject]
        next_offset: str | None
        users: list[TLObject]
        def __init__(self, *, count: int, boosts: list[TLObject], next_offset: str | None = ..., users: list[TLObject]) -> None: ...

    class boostsStatus(TLObject):
        my_boost: bool
        level: int
        current_level_boosts: int
        boosts: int
        gift_boosts: int | None
        next_level_boosts: int | None
        premium_audience: TLObject | None
        boost_url: str
        prepaid_giveaways: list[TLObject] | None
        my_boost_slots: list[int] | None
        def __init__(self, *, my_boost: bool = ..., level: int, current_level_boosts: int, boosts: int, gift_boosts: int | None = ..., next_level_boosts: int | None = ..., premium_audience: TLObject | None = ..., boost_url: str, prepaid_giveaways: list[TLObject] | None = ..., my_boost_slots: list[int] | None = ...) -> None: ...

    class getBoostsList(TLObject):
        gifts: bool
        peer: TLObject
        offset: str
        limit: int
        def __init__(self, *, gifts: bool = ..., peer: TLObject, offset: str, limit: int) -> None: ...

    class getBoostsStatus(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getMyBoosts(TLObject):
        def __init__(self) -> None: ...

    class getUserBoosts(TLObject):
        peer: TLObject
        user_id: TLObject
        def __init__(self, *, peer: TLObject, user_id: TLObject) -> None: ...

    class myBoosts(TLObject):
        my_boosts: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, my_boosts: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

class premiumGiftCodeOption(TLObject):
    users: int
    months: int
    store_product: str | None
    store_quantity: int | None
    currency: str
    amount: int
    def __init__(self, *, users: int, months: int, store_product: str | None = ..., store_quantity: int | None = ..., currency: str, amount: int) -> None: ...

class premiumSubscriptionOption(TLObject):
    current: bool
    can_purchase_upgrade: bool
    transaction: str | None
    months: int
    currency: str
    amount: int
    bot_url: str
    store_product: str | None
    def __init__(self, *, current: bool = ..., can_purchase_upgrade: bool = ..., transaction: str | None = ..., months: int, currency: str, amount: int, bot_url: str, store_product: str | None = ...) -> None: ...

class prepaidGiveaway(TLObject):
    id: int
    months: int
    quantity: int
    date: int
    def __init__(self, *, id: int, months: int, quantity: int, date: int) -> None: ...

class prepaidStarsGiveaway(TLObject):
    id: int
    stars: int
    quantity: int
    boosts: int
    date: int
    def __init__(self, *, id: int, stars: int, quantity: int, boosts: int, date: int) -> None: ...

class privacyKeyAbout(TLObject):
    def __init__(self) -> None: ...

class privacyKeyAddedByPhone(TLObject):
    def __init__(self) -> None: ...

class privacyKeyBirthday(TLObject):
    def __init__(self) -> None: ...

class privacyKeyChatInvite(TLObject):
    def __init__(self) -> None: ...

class privacyKeyForwards(TLObject):
    def __init__(self) -> None: ...

class privacyKeyNoPaidMessages(TLObject):
    def __init__(self) -> None: ...

class privacyKeyPhoneCall(TLObject):
    def __init__(self) -> None: ...

class privacyKeyPhoneNumber(TLObject):
    def __init__(self) -> None: ...

class privacyKeyPhoneP2P(TLObject):
    def __init__(self) -> None: ...

class privacyKeyProfilePhoto(TLObject):
    def __init__(self) -> None: ...

class privacyKeySavedMusic(TLObject):
    def __init__(self) -> None: ...

class privacyKeyStarGiftsAutoSave(TLObject):
    def __init__(self) -> None: ...

class privacyKeyStatusTimestamp(TLObject):
    def __init__(self) -> None: ...

class privacyKeyVoiceMessages(TLObject):
    def __init__(self) -> None: ...

class privacyValueAllowAll(TLObject):
    def __init__(self) -> None: ...

class privacyValueAllowBots(TLObject):
    def __init__(self) -> None: ...

class privacyValueAllowChatParticipants(TLObject):
    chats: list[int]
    def __init__(self, *, chats: list[int]) -> None: ...

class privacyValueAllowCloseFriends(TLObject):
    def __init__(self) -> None: ...

class privacyValueAllowContacts(TLObject):
    def __init__(self) -> None: ...

class privacyValueAllowPremium(TLObject):
    def __init__(self) -> None: ...

class privacyValueAllowUsers(TLObject):
    users: list[int]
    def __init__(self, *, users: list[int]) -> None: ...

class privacyValueDisallowAll(TLObject):
    def __init__(self) -> None: ...

class privacyValueDisallowBots(TLObject):
    def __init__(self) -> None: ...

class privacyValueDisallowChatParticipants(TLObject):
    chats: list[int]
    def __init__(self, *, chats: list[int]) -> None: ...

class privacyValueDisallowContacts(TLObject):
    def __init__(self) -> None: ...

class privacyValueDisallowUsers(TLObject):
    users: list[int]
    def __init__(self, *, users: list[int]) -> None: ...

class profileTabFiles(TLObject):
    def __init__(self) -> None: ...

class profileTabGifs(TLObject):
    def __init__(self) -> None: ...

class profileTabGifts(TLObject):
    def __init__(self) -> None: ...

class profileTabLinks(TLObject):
    def __init__(self) -> None: ...

class profileTabMedia(TLObject):
    def __init__(self) -> None: ...

class profileTabMusic(TLObject):
    def __init__(self) -> None: ...

class profileTabPosts(TLObject):
    def __init__(self) -> None: ...

class profileTabVoice(TLObject):
    def __init__(self) -> None: ...

class publicForwardMessage(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class publicForwardStory(TLObject):
    peer: TLObject
    story: TLObject
    def __init__(self, *, peer: TLObject, story: TLObject) -> None: ...

class quickReply(TLObject):
    shortcut_id: int
    shortcut: str
    top_message: int
    count: int
    def __init__(self, *, shortcut_id: int, shortcut: str, top_message: int, count: int) -> None: ...

class reactionCount(TLObject):
    chosen_order: int | None
    reaction: TLObject
    count: int
    def __init__(self, *, chosen_order: int | None = ..., reaction: TLObject, count: int) -> None: ...

class reactionCustomEmoji(TLObject):
    document_id: int
    def __init__(self, *, document_id: int) -> None: ...

class reactionEmoji(TLObject):
    emoticon: str
    def __init__(self, *, emoticon: str) -> None: ...

class reactionEmpty(TLObject):
    def __init__(self) -> None: ...

class reactionNotificationsFromAll(TLObject):
    def __init__(self) -> None: ...

class reactionNotificationsFromContacts(TLObject):
    def __init__(self) -> None: ...

class reactionPaid(TLObject):
    def __init__(self) -> None: ...

class reactionsNotifySettings(TLObject):
    messages_notify_from: TLObject | None
    stories_notify_from: TLObject | None
    poll_votes_notify_from: TLObject | None
    sound: TLObject
    show_previews: bool
    def __init__(self, *, messages_notify_from: TLObject | None = ..., stories_notify_from: TLObject | None = ..., poll_votes_notify_from: TLObject | None = ..., sound: TLObject, show_previews: bool) -> None: ...

class readParticipantDate(TLObject):
    user_id: int
    date: int
    def __init__(self, *, user_id: int, date: int) -> None: ...

class receivedNotifyMessage(TLObject):
    id: int
    flags: int
    def __init__(self, *, id: int, flags: int) -> None: ...

class recentMeUrlChat(TLObject):
    url: str
    chat_id: int
    def __init__(self, *, url: str, chat_id: int) -> None: ...

class recentMeUrlChatInvite(TLObject):
    url: str
    chat_invite: TLObject
    def __init__(self, *, url: str, chat_invite: TLObject) -> None: ...

class recentMeUrlStickerSet(TLObject):
    url: str
    set: TLObject
    def __init__(self, *, url: str, set: TLObject) -> None: ...

class recentMeUrlUnknown(TLObject):
    url: str
    def __init__(self, *, url: str) -> None: ...

class recentMeUrlUser(TLObject):
    url: str
    user_id: int
    def __init__(self, *, url: str, user_id: int) -> None: ...

class recentStory(TLObject):
    live: bool
    max_id: int | None
    def __init__(self, *, live: bool = ..., max_id: int | None = ...) -> None: ...

class replyInlineMarkup(TLObject):
    force_reply: bool
    rows: list[TLObject]
    def __init__(self, *, force_reply: bool = ..., rows: list[TLObject]) -> None: ...

class replyKeyboardForceReply(TLObject):
    single_use: bool
    selective: bool
    placeholder: str | None
    def __init__(self, *, single_use: bool = ..., selective: bool = ..., placeholder: str | None = ...) -> None: ...

class replyKeyboardHide(TLObject):
    selective: bool
    def __init__(self, *, selective: bool = ...) -> None: ...

class replyKeyboardMarkup(TLObject):
    resize: bool
    single_use: bool
    selective: bool
    persistent: bool
    force_reply: bool
    rows: list[TLObject]
    placeholder: str | None
    def __init__(self, *, resize: bool = ..., single_use: bool = ..., selective: bool = ..., persistent: bool = ..., force_reply: bool = ..., rows: list[TLObject], placeholder: str | None = ...) -> None: ...

class reportResultAddComment(TLObject):
    optional: bool
    option: bytes
    def __init__(self, *, optional: bool = ..., option: bytes) -> None: ...

class reportResultChooseOption(TLObject):
    title: str
    options: list[TLObject]
    def __init__(self, *, title: str, options: list[TLObject]) -> None: ...

class reportResultReported(TLObject):
    def __init__(self) -> None: ...

class requestPeerTypeBroadcast(TLObject):
    creator: bool
    has_username: bool
    user_admin_rights: TLObject | None
    bot_admin_rights: TLObject | None
    def __init__(self, *, creator: bool = ..., has_username: bool = ..., user_admin_rights: TLObject | None = ..., bot_admin_rights: TLObject | None = ...) -> None: ...

class requestPeerTypeChat(TLObject):
    creator: bool
    bot_participant: bool
    has_username: bool
    forum: bool
    user_admin_rights: TLObject | None
    bot_admin_rights: TLObject | None
    def __init__(self, *, creator: bool = ..., bot_participant: bool = ..., has_username: bool = ..., forum: bool = ..., user_admin_rights: TLObject | None = ..., bot_admin_rights: TLObject | None = ...) -> None: ...

class requestPeerTypeCreateBot(TLObject):
    bot_managed: bool
    suggested_name: str | None
    suggested_username: str | None
    def __init__(self, *, bot_managed: bool = ..., suggested_name: str | None = ..., suggested_username: str | None = ...) -> None: ...

class requestPeerTypeUser(TLObject):
    bot: bool
    premium: bool
    def __init__(self, *, bot: bool = ..., premium: bool = ...) -> None: ...

class requestedPeerChannel(TLObject):
    channel_id: int
    title: str | None
    username: str | None
    photo: TLObject | None
    def __init__(self, *, channel_id: int, title: str | None = ..., username: str | None = ..., photo: TLObject | None = ...) -> None: ...

class requestedPeerChat(TLObject):
    chat_id: int
    title: str | None
    photo: TLObject | None
    def __init__(self, *, chat_id: int, title: str | None = ..., photo: TLObject | None = ...) -> None: ...

class requestedPeerUser(TLObject):
    user_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    photo: TLObject | None
    def __init__(self, *, user_id: int, first_name: str | None = ..., last_name: str | None = ..., username: str | None = ..., photo: TLObject | None = ...) -> None: ...

class requirementToContactEmpty(TLObject):
    def __init__(self) -> None: ...

class requirementToContactPaidMessages(TLObject):
    stars_amount: int
    def __init__(self, *, stars_amount: int) -> None: ...

class requirementToContactPremium(TLObject):
    def __init__(self) -> None: ...

class restrictionReason(TLObject):
    platform: str
    reason: str
    text: str
    def __init__(self, *, platform: str, reason: str, text: str) -> None: ...

class richButtonStyle(TLObject):
    bg_primary: bool
    bg_danger: bool
    bg_success: bool
    link: bool
    def __init__(self, *, bg_primary: bool = ..., bg_danger: bool = ..., bg_success: bool = ..., link: bool = ...) -> None: ...

class richMessage(TLObject):
    rtl: bool
    part: bool
    blocks: list[TLObject]
    photos: list[TLObject]
    documents: list[TLObject]
    def __init__(self, *, rtl: bool = ..., part: bool = ..., blocks: list[TLObject], photos: list[TLObject], documents: list[TLObject]) -> None: ...

class savedDialog(TLObject):
    pinned: bool
    peer: TLObject
    top_message: int
    def __init__(self, *, pinned: bool = ..., peer: TLObject, top_message: int) -> None: ...

class savedPhoneContact(TLObject):
    phone: str
    first_name: str
    last_name: str
    date: int
    def __init__(self, *, phone: str, first_name: str, last_name: str, date: int) -> None: ...

class savedReactionTag(TLObject):
    reaction: TLObject
    title: str | None
    count: int
    def __init__(self, *, reaction: TLObject, title: str | None = ..., count: int) -> None: ...

class savedStarGift(TLObject):
    name_hidden: bool
    unsaved: bool
    refunded: bool
    can_upgrade: bool
    pinned_to_top: bool
    upgrade_separate: bool
    from_id: TLObject | None
    date: int
    gift: TLObject
    message: TLObject | None
    msg_id: int | None
    saved_id: int | None
    convert_stars: int | None
    upgrade_stars: int | None
    can_export_at: int | None
    transfer_stars: int | None
    can_transfer_at: int | None
    can_resell_at: int | None
    collection_id: list[int] | None
    prepaid_upgrade_hash: str | None
    drop_original_details_stars: int | None
    gift_num: int | None
    can_craft_at: int | None
    def __init__(self, *, name_hidden: bool = ..., unsaved: bool = ..., refunded: bool = ..., can_upgrade: bool = ..., pinned_to_top: bool = ..., upgrade_separate: bool = ..., from_id: TLObject | None = ..., date: int, gift: TLObject, message: TLObject | None = ..., msg_id: int | None = ..., saved_id: int | None = ..., convert_stars: int | None = ..., upgrade_stars: int | None = ..., can_export_at: int | None = ..., transfer_stars: int | None = ..., can_transfer_at: int | None = ..., can_resell_at: int | None = ..., collection_id: list[int] | None = ..., prepaid_upgrade_hash: str | None = ..., drop_original_details_stars: int | None = ..., gift_num: int | None = ..., can_craft_at: int | None = ...) -> None: ...

class searchPostsFlood(TLObject):
    query_is_free: bool
    total_daily: int
    remains: int
    wait_till: int | None
    stars_amount: int
    def __init__(self, *, query_is_free: bool = ..., total_daily: int, remains: int, wait_till: int | None = ..., stars_amount: int) -> None: ...

class searchResultPosition(TLObject):
    msg_id: int
    date: int
    offset: int
    def __init__(self, *, msg_id: int, date: int, offset: int) -> None: ...

class searchResultsCalendarPeriod(TLObject):
    date: int
    min_msg_id: int
    max_msg_id: int
    count: int
    def __init__(self, *, date: int, min_msg_id: int, max_msg_id: int, count: int) -> None: ...

class secureCredentialsEncrypted(TLObject):
    data: bytes
    hash: bytes
    secret: bytes
    def __init__(self, *, data: bytes, hash: bytes, secret: bytes) -> None: ...

class secureData(TLObject):
    data: bytes
    data_hash: bytes
    secret: bytes
    def __init__(self, *, data: bytes, data_hash: bytes, secret: bytes) -> None: ...

class secureFile(TLObject):
    id: int
    access_hash: int
    size: int
    dc_id: int
    date: int
    file_hash: bytes
    secret: bytes
    def __init__(self, *, id: int, access_hash: int, size: int, dc_id: int, date: int, file_hash: bytes, secret: bytes) -> None: ...

class secureFileEmpty(TLObject):
    def __init__(self) -> None: ...

class securePasswordKdfAlgoPBKDF2HMACSHA512iter100000(TLObject):
    salt: bytes
    def __init__(self, *, salt: bytes) -> None: ...

class securePasswordKdfAlgoSHA512(TLObject):
    salt: bytes
    def __init__(self, *, salt: bytes) -> None: ...

class securePasswordKdfAlgoUnknown(TLObject):
    def __init__(self) -> None: ...

class securePlainEmail(TLObject):
    email: str
    def __init__(self, *, email: str) -> None: ...

class securePlainPhone(TLObject):
    phone: str
    def __init__(self, *, phone: str) -> None: ...

class secureRequiredType(TLObject):
    native_names: bool
    selfie_required: bool
    translation_required: bool
    type: TLObject
    def __init__(self, *, native_names: bool = ..., selfie_required: bool = ..., translation_required: bool = ..., type: TLObject) -> None: ...

class secureRequiredTypeOneOf(TLObject):
    types: list[TLObject]
    def __init__(self, *, types: list[TLObject]) -> None: ...

class secureSecretSettings(TLObject):
    secure_algo: TLObject
    secure_secret: bytes
    secure_secret_id: int
    def __init__(self, *, secure_algo: TLObject, secure_secret: bytes, secure_secret_id: int) -> None: ...

class secureValue(TLObject):
    type: TLObject
    data: TLObject | None
    front_side: TLObject | None
    reverse_side: TLObject | None
    selfie: TLObject | None
    translation: list[TLObject] | None
    files: list[TLObject] | None
    plain_data: TLObject | None
    hash: bytes
    def __init__(self, *, type: TLObject, data: TLObject | None = ..., front_side: TLObject | None = ..., reverse_side: TLObject | None = ..., selfie: TLObject | None = ..., translation: list[TLObject] | None = ..., files: list[TLObject] | None = ..., plain_data: TLObject | None = ..., hash: bytes) -> None: ...

class secureValueError(TLObject):
    type: TLObject
    hash: bytes
    text: str
    def __init__(self, *, type: TLObject, hash: bytes, text: str) -> None: ...

class secureValueErrorData(TLObject):
    type: TLObject
    data_hash: bytes
    field: str
    text: str
    def __init__(self, *, type: TLObject, data_hash: bytes, field: str, text: str) -> None: ...

class secureValueErrorFile(TLObject):
    type: TLObject
    file_hash: bytes
    text: str
    def __init__(self, *, type: TLObject, file_hash: bytes, text: str) -> None: ...

class secureValueErrorFiles(TLObject):
    type: TLObject
    file_hash: list[bytes]
    text: str
    def __init__(self, *, type: TLObject, file_hash: list[bytes], text: str) -> None: ...

class secureValueErrorFrontSide(TLObject):
    type: TLObject
    file_hash: bytes
    text: str
    def __init__(self, *, type: TLObject, file_hash: bytes, text: str) -> None: ...

class secureValueErrorReverseSide(TLObject):
    type: TLObject
    file_hash: bytes
    text: str
    def __init__(self, *, type: TLObject, file_hash: bytes, text: str) -> None: ...

class secureValueErrorSelfie(TLObject):
    type: TLObject
    file_hash: bytes
    text: str
    def __init__(self, *, type: TLObject, file_hash: bytes, text: str) -> None: ...

class secureValueErrorTranslationFile(TLObject):
    type: TLObject
    file_hash: bytes
    text: str
    def __init__(self, *, type: TLObject, file_hash: bytes, text: str) -> None: ...

class secureValueErrorTranslationFiles(TLObject):
    type: TLObject
    file_hash: list[bytes]
    text: str
    def __init__(self, *, type: TLObject, file_hash: list[bytes], text: str) -> None: ...

class secureValueHash(TLObject):
    type: TLObject
    hash: bytes
    def __init__(self, *, type: TLObject, hash: bytes) -> None: ...

class secureValueTypeAddress(TLObject):
    def __init__(self) -> None: ...

class secureValueTypeBankStatement(TLObject):
    def __init__(self) -> None: ...

class secureValueTypeDriverLicense(TLObject):
    def __init__(self) -> None: ...

class secureValueTypeEmail(TLObject):
    def __init__(self) -> None: ...

class secureValueTypeIdentityCard(TLObject):
    def __init__(self) -> None: ...

class secureValueTypeInternalPassport(TLObject):
    def __init__(self) -> None: ...

class secureValueTypePassport(TLObject):
    def __init__(self) -> None: ...

class secureValueTypePassportRegistration(TLObject):
    def __init__(self) -> None: ...

class secureValueTypePersonalDetails(TLObject):
    def __init__(self) -> None: ...

class secureValueTypePhone(TLObject):
    def __init__(self) -> None: ...

class secureValueTypeRentalAgreement(TLObject):
    def __init__(self) -> None: ...

class secureValueTypeTemporaryRegistration(TLObject):
    def __init__(self) -> None: ...

class secureValueTypeUtilityBill(TLObject):
    def __init__(self) -> None: ...

class sendAsPeer(TLObject):
    premium_required: bool
    peer: TLObject
    def __init__(self, *, premium_required: bool = ..., peer: TLObject) -> None: ...

class sendMessageCancelAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageChooseContactAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageChooseStickerAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageEmojiInteraction(TLObject):
    emoticon: str
    msg_id: int
    interaction: TLObject
    def __init__(self, *, emoticon: str, msg_id: int, interaction: TLObject) -> None: ...

class sendMessageEmojiInteractionSeen(TLObject):
    emoticon: str
    def __init__(self, *, emoticon: str) -> None: ...

class sendMessageGamePlayAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageGeoLocationAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageHistoryImportAction(TLObject):
    progress: int
    def __init__(self, *, progress: int) -> None: ...

class sendMessageRecordAudioAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageRecordRoundAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageRecordVideoAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageRichMessageDraftAction(TLObject):
    can_stop: bool
    keep_on_stop: bool
    random_id: int
    rich_message: TLObject
    def __init__(self, *, can_stop: bool = ..., keep_on_stop: bool = ..., random_id: int, rich_message: TLObject) -> None: ...

class sendMessageStopDraftAction(TLObject):
    random_id: int
    def __init__(self, *, random_id: int) -> None: ...

class sendMessageTextDraftAction(TLObject):
    can_stop: bool
    keep_on_stop: bool
    random_id: int
    text: TLObject
    def __init__(self, *, can_stop: bool = ..., keep_on_stop: bool = ..., random_id: int, text: TLObject) -> None: ...

class sendMessageTypingAction(TLObject):
    def __init__(self) -> None: ...

class sendMessageUploadAudioAction(TLObject):
    progress: int
    def __init__(self, *, progress: int) -> None: ...

class sendMessageUploadDocumentAction(TLObject):
    progress: int
    def __init__(self, *, progress: int) -> None: ...

class sendMessageUploadPhotoAction(TLObject):
    progress: int
    def __init__(self, *, progress: int) -> None: ...

class sendMessageUploadRoundAction(TLObject):
    progress: int
    def __init__(self, *, progress: int) -> None: ...

class sendMessageUploadVideoAction(TLObject):
    progress: int
    def __init__(self, *, progress: int) -> None: ...

class shareThemeBackdropOption(TLObject):
    backdrop_id: int
    name: str
    center_color: int
    edge_color: int
    pattern_color: int
    text_color: int
    def __init__(self, *, backdrop_id: int, name: str, center_color: int, edge_color: int, pattern_color: int, text_color: int) -> None: ...

class shareThemeBackdrops(TLObject):
    hash: int
    backdrops: list[TLObject]
    def __init__(self, *, hash: int, backdrops: list[TLObject]) -> None: ...

class shareThemeBackdropsNotModified(TLObject):
    def __init__(self) -> None: ...

class shareThemeDefault(TLObject):
    def __init__(self) -> None: ...

class shareThemeEmojiBackdrop(TLObject):
    backdrop_id: int | None
    emojis: list[TLObject] | None
    def __init__(self, *, backdrop_id: int | None = ..., emojis: list[TLObject] | None = ...) -> None: ...

class shareThemeGift(TLObject):
    stargift: TLObject
    def __init__(self, *, stargift: TLObject) -> None: ...

class shippingOption(TLObject):
    id: str
    title: str
    prices: list[TLObject]
    def __init__(self, *, id: str, title: str, prices: list[TLObject]) -> None: ...

class smsJob(TLObject):
    job_id: str
    phone_number: str
    text: str
    def __init__(self, *, job_id: str, phone_number: str, text: str) -> None: ...

class smsjobs:
    class eligibleToJoin(TLObject):
        terms_url: str
        monthly_sent_sms: int
        def __init__(self, *, terms_url: str, monthly_sent_sms: int) -> None: ...

    class finishJob(TLObject):
        job_id: str
        error: str | None
        def __init__(self, *, job_id: str, error: str | None = ...) -> None: ...

    class getSmsJob(TLObject):
        job_id: str
        def __init__(self, *, job_id: str) -> None: ...

    class getStatus(TLObject):
        def __init__(self) -> None: ...

    class isEligibleToJoin(TLObject):
        def __init__(self) -> None: ...

    class join(TLObject):
        def __init__(self) -> None: ...

    class leave(TLObject):
        def __init__(self) -> None: ...

    class status(TLObject):
        allow_international: bool
        recent_sent: int
        recent_since: int
        recent_remains: int
        total_sent: int
        total_since: int
        last_gift_slug: str | None
        terms_url: str
        def __init__(self, *, allow_international: bool = ..., recent_sent: int, recent_since: int, recent_remains: int, total_sent: int, total_since: int, last_gift_slug: str | None = ..., terms_url: str) -> None: ...

    class updateSettings(TLObject):
        allow_international: bool
        def __init__(self, *, allow_international: bool = ...) -> None: ...

class speakingInGroupCallAction(TLObject):
    def __init__(self) -> None: ...

class sponsoredMessage(TLObject):
    recommended: bool
    can_report: bool
    random_id: bytes
    url: str
    title: str
    message: str
    entities: list[TLObject] | None
    photo: TLObject | None
    media: TLObject | None
    color: TLObject | None
    button_text: str
    sponsor_info: str | None
    additional_info: str | None
    min_display_duration: int | None
    max_display_duration: int | None
    def __init__(self, *, recommended: bool = ..., can_report: bool = ..., random_id: bytes, url: str, title: str, message: str, entities: list[TLObject] | None = ..., photo: TLObject | None = ..., media: TLObject | None = ..., color: TLObject | None = ..., button_text: str, sponsor_info: str | None = ..., additional_info: str | None = ..., min_display_duration: int | None = ..., max_display_duration: int | None = ...) -> None: ...

class sponsoredMessageReportOption(TLObject):
    text: str
    option: bytes
    def __init__(self, *, text: str, option: bytes) -> None: ...

class sponsoredPeer(TLObject):
    random_id: bytes
    peer: TLObject
    sponsor_info: str | None
    additional_info: str | None
    def __init__(self, *, random_id: bytes, peer: TLObject, sponsor_info: str | None = ..., additional_info: str | None = ...) -> None: ...

class starGift(TLObject):
    limited: bool
    sold_out: bool
    birthday: bool
    require_premium: bool
    limited_per_user: bool
    peer_color_available: bool
    auction: bool
    id: int
    sticker: TLObject
    stars: int
    availability_remains: int | None
    availability_total: int | None
    availability_resale: int | None
    convert_stars: int
    first_sale_date: int | None
    last_sale_date: int | None
    upgrade_stars: int | None
    resell_min_stars: int | None
    title: str | None
    released_by: TLObject | None
    per_user_total: int | None
    per_user_remains: int | None
    locked_until_date: int | None
    auction_slug: str | None
    gifts_per_round: int | None
    auction_start_date: int | None
    upgrade_variants: int | None
    background: TLObject | None
    def __init__(self, *, limited: bool = ..., sold_out: bool = ..., birthday: bool = ..., require_premium: bool = ..., limited_per_user: bool = ..., peer_color_available: bool = ..., auction: bool = ..., id: int, sticker: TLObject, stars: int, availability_remains: int | None = ..., availability_total: int | None = ..., availability_resale: int | None = ..., convert_stars: int, first_sale_date: int | None = ..., last_sale_date: int | None = ..., upgrade_stars: int | None = ..., resell_min_stars: int | None = ..., title: str | None = ..., released_by: TLObject | None = ..., per_user_total: int | None = ..., per_user_remains: int | None = ..., locked_until_date: int | None = ..., auction_slug: str | None = ..., gifts_per_round: int | None = ..., auction_start_date: int | None = ..., upgrade_variants: int | None = ..., background: TLObject | None = ...) -> None: ...

class starGiftActiveAuctionState(TLObject):
    gift: TLObject
    state: TLObject
    user_state: TLObject
    def __init__(self, *, gift: TLObject, state: TLObject, user_state: TLObject) -> None: ...

class starGiftAttributeBackdrop(TLObject):
    name: str
    backdrop_id: int
    center_color: int
    edge_color: int
    pattern_color: int
    text_color: int
    rarity: TLObject
    def __init__(self, *, name: str, backdrop_id: int, center_color: int, edge_color: int, pattern_color: int, text_color: int, rarity: TLObject) -> None: ...

class starGiftAttributeCounter(TLObject):
    attribute: TLObject
    count: int
    def __init__(self, *, attribute: TLObject, count: int) -> None: ...

class starGiftAttributeIdBackdrop(TLObject):
    backdrop_id: int
    def __init__(self, *, backdrop_id: int) -> None: ...

class starGiftAttributeIdModel(TLObject):
    document_id: int
    def __init__(self, *, document_id: int) -> None: ...

class starGiftAttributeIdPattern(TLObject):
    document_id: int
    def __init__(self, *, document_id: int) -> None: ...

class starGiftAttributeModel(TLObject):
    crafted: bool
    name: str
    document: TLObject
    rarity: TLObject
    def __init__(self, *, crafted: bool = ..., name: str, document: TLObject, rarity: TLObject) -> None: ...

class starGiftAttributeOriginalDetails(TLObject):
    sender_id: TLObject | None
    recipient_id: TLObject
    date: int
    message: TLObject | None
    def __init__(self, *, sender_id: TLObject | None = ..., recipient_id: TLObject, date: int, message: TLObject | None = ...) -> None: ...

class starGiftAttributePattern(TLObject):
    name: str
    document: TLObject
    rarity: TLObject
    def __init__(self, *, name: str, document: TLObject, rarity: TLObject) -> None: ...

class starGiftAttributeRarity(TLObject):
    permille: int
    def __init__(self, *, permille: int) -> None: ...

class starGiftAttributeRarityEpic(TLObject):
    def __init__(self) -> None: ...

class starGiftAttributeRarityLegendary(TLObject):
    def __init__(self) -> None: ...

class starGiftAttributeRarityRare(TLObject):
    def __init__(self) -> None: ...

class starGiftAttributeRarityUncommon(TLObject):
    def __init__(self) -> None: ...

class starGiftAuctionAcquiredGift(TLObject):
    name_hidden: bool
    peer: TLObject
    date: int
    bid_amount: int
    round: int
    pos: int
    message: TLObject | None
    gift_num: int | None
    def __init__(self, *, name_hidden: bool = ..., peer: TLObject, date: int, bid_amount: int, round: int, pos: int, message: TLObject | None = ..., gift_num: int | None = ...) -> None: ...

class starGiftAuctionRound(TLObject):
    num: int
    duration: int
    def __init__(self, *, num: int, duration: int) -> None: ...

class starGiftAuctionRoundExtendable(TLObject):
    num: int
    duration: int
    extend_top: int
    extend_window: int
    def __init__(self, *, num: int, duration: int, extend_top: int, extend_window: int) -> None: ...

class starGiftAuctionState(TLObject):
    version: int
    start_date: int
    end_date: int
    min_bid_amount: int
    bid_levels: list[TLObject]
    top_bidders: list[int]
    next_round_at: int
    last_gift_num: int
    gifts_left: int
    current_round: int
    total_rounds: int
    rounds: list[TLObject]
    def __init__(self, *, version: int, start_date: int, end_date: int, min_bid_amount: int, bid_levels: list[TLObject], top_bidders: list[int], next_round_at: int, last_gift_num: int, gifts_left: int, current_round: int, total_rounds: int, rounds: list[TLObject]) -> None: ...

class starGiftAuctionStateFinished(TLObject):
    start_date: int
    end_date: int
    average_price: int
    listed_count: int | None
    fragment_listed_count: int | None
    fragment_listed_url: str | None
    def __init__(self, *, start_date: int, end_date: int, average_price: int, listed_count: int | None = ..., fragment_listed_count: int | None = ..., fragment_listed_url: str | None = ...) -> None: ...

class starGiftAuctionStateNotModified(TLObject):
    def __init__(self) -> None: ...

class starGiftAuctionUserState(TLObject):
    returned: bool
    bid_amount: int | None
    bid_date: int | None
    min_bid_amount: int | None
    bid_peer: TLObject | None
    acquired_count: int
    def __init__(self, *, returned: bool = ..., bid_amount: int | None = ..., bid_date: int | None = ..., min_bid_amount: int | None = ..., bid_peer: TLObject | None = ..., acquired_count: int) -> None: ...

class starGiftBackground(TLObject):
    center_color: int
    edge_color: int
    text_color: int
    def __init__(self, *, center_color: int, edge_color: int, text_color: int) -> None: ...

class starGiftCollection(TLObject):
    collection_id: int
    title: str
    icon: TLObject | None
    gifts_count: int
    hash: int
    def __init__(self, *, collection_id: int, title: str, icon: TLObject | None = ..., gifts_count: int, hash: int) -> None: ...

class starGiftUnique(TLObject):
    require_premium: bool
    resale_ton_only: bool
    theme_available: bool
    burned: bool
    crafted: bool
    id: int
    gift_id: int
    title: str
    slug: str
    num: int
    owner_id: TLObject | None
    owner_name: str | None
    owner_address: str | None
    attributes: list[TLObject]
    availability_issued: int
    availability_total: int
    gift_address: str | None
    resell_amount: list[TLObject] | None
    released_by: TLObject | None
    value_amount: int | None
    value_currency: str | None
    value_usd_amount: int | None
    theme_peer: TLObject | None
    peer_color: TLObject | None
    host_id: TLObject | None
    offer_min_stars: int | None
    craft_chance_permille: int | None
    def __init__(self, *, require_premium: bool = ..., resale_ton_only: bool = ..., theme_available: bool = ..., burned: bool = ..., crafted: bool = ..., id: int, gift_id: int, title: str, slug: str, num: int, owner_id: TLObject | None = ..., owner_name: str | None = ..., owner_address: str | None = ..., attributes: list[TLObject], availability_issued: int, availability_total: int, gift_address: str | None = ..., resell_amount: list[TLObject] | None = ..., released_by: TLObject | None = ..., value_amount: int | None = ..., value_currency: str | None = ..., value_usd_amount: int | None = ..., theme_peer: TLObject | None = ..., peer_color: TLObject | None = ..., host_id: TLObject | None = ..., offer_min_stars: int | None = ..., craft_chance_permille: int | None = ...) -> None: ...

class starGiftUpgradePrice(TLObject):
    date: int
    upgrade_stars: int
    def __init__(self, *, date: int, upgrade_stars: int) -> None: ...

class starRefProgram(TLObject):
    bot_id: int
    commission_permille: int
    duration_months: int | None
    end_date: int | None
    daily_revenue_per_user: TLObject | None
    def __init__(self, *, bot_id: int, commission_permille: int, duration_months: int | None = ..., end_date: int | None = ..., daily_revenue_per_user: TLObject | None = ...) -> None: ...

class starsAmount(TLObject):
    amount: int
    nanos: int
    def __init__(self, *, amount: int, nanos: int) -> None: ...

class starsGiftOption(TLObject):
    extended: bool
    stars: int
    store_product: str | None
    currency: str
    amount: int
    def __init__(self, *, extended: bool = ..., stars: int, store_product: str | None = ..., currency: str, amount: int) -> None: ...

class starsGiveawayOption(TLObject):
    extended: bool
    default: bool
    stars: int
    yearly_boosts: int
    store_product: str | None
    currency: str
    amount: int
    winners: list[TLObject]
    def __init__(self, *, extended: bool = ..., default: bool = ..., stars: int, yearly_boosts: int, store_product: str | None = ..., currency: str, amount: int, winners: list[TLObject]) -> None: ...

class starsGiveawayWinnersOption(TLObject):
    default: bool
    users: int
    per_user_stars: int
    def __init__(self, *, default: bool = ..., users: int, per_user_stars: int) -> None: ...

class starsRating(TLObject):
    level: int
    current_level_stars: int
    stars: int
    next_level_stars: int | None
    def __init__(self, *, level: int, current_level_stars: int, stars: int, next_level_stars: int | None = ...) -> None: ...

class starsRevenueStatus(TLObject):
    withdrawal_enabled: bool
    current_balance: TLObject
    available_balance: TLObject
    overall_revenue: TLObject
    next_withdrawal_at: int | None
    def __init__(self, *, withdrawal_enabled: bool = ..., current_balance: TLObject, available_balance: TLObject, overall_revenue: TLObject, next_withdrawal_at: int | None = ...) -> None: ...

class starsSubscription(TLObject):
    canceled: bool
    can_refulfill: bool
    missing_balance: bool
    bot_canceled: bool
    id: str
    peer: TLObject
    until_date: int
    pricing: TLObject
    chat_invite_hash: str | None
    title: str | None
    photo: TLObject | None
    invoice_slug: str | None
    def __init__(self, *, canceled: bool = ..., can_refulfill: bool = ..., missing_balance: bool = ..., bot_canceled: bool = ..., id: str, peer: TLObject, until_date: int, pricing: TLObject, chat_invite_hash: str | None = ..., title: str | None = ..., photo: TLObject | None = ..., invoice_slug: str | None = ...) -> None: ...

class starsSubscriptionPricing(TLObject):
    period: int
    amount: int
    def __init__(self, *, period: int, amount: int) -> None: ...

class starsTonAmount(TLObject):
    amount: int
    def __init__(self, *, amount: int) -> None: ...

class starsTopupOption(TLObject):
    extended: bool
    stars: int
    store_product: str | None
    currency: str
    amount: int
    def __init__(self, *, extended: bool = ..., stars: int, store_product: str | None = ..., currency: str, amount: int) -> None: ...

class starsTransaction(TLObject):
    refund: bool
    pending: bool
    failed: bool
    gift: bool
    reaction: bool
    stargift_upgrade: bool
    business_transfer: bool
    stargift_resale: bool
    posts_search: bool
    stargift_prepaid_upgrade: bool
    stargift_drop_original_details: bool
    phonegroup_message: bool
    stargift_auction_bid: bool
    offer: bool
    id: str
    amount: TLObject
    date: int
    peer: TLObject
    title: str | None
    description: str | None
    photo: TLObject | None
    transaction_date: int | None
    transaction_url: str | None
    bot_payload: bytes | None
    msg_id: int | None
    extended_media: list[TLObject] | None
    subscription_period: int | None
    giveaway_post_id: int | None
    stargift: TLObject | None
    floodskip_number: int | None
    starref_commission_permille: int | None
    starref_peer: TLObject | None
    starref_amount: TLObject | None
    paid_messages: int | None
    premium_gift_months: int | None
    ads_proceeds_from_date: int | None
    ads_proceeds_to_date: int | None
    def __init__(self, *, refund: bool = ..., pending: bool = ..., failed: bool = ..., gift: bool = ..., reaction: bool = ..., stargift_upgrade: bool = ..., business_transfer: bool = ..., stargift_resale: bool = ..., posts_search: bool = ..., stargift_prepaid_upgrade: bool = ..., stargift_drop_original_details: bool = ..., phonegroup_message: bool = ..., stargift_auction_bid: bool = ..., offer: bool = ..., id: str, amount: TLObject, date: int, peer: TLObject, title: str | None = ..., description: str | None = ..., photo: TLObject | None = ..., transaction_date: int | None = ..., transaction_url: str | None = ..., bot_payload: bytes | None = ..., msg_id: int | None = ..., extended_media: list[TLObject] | None = ..., subscription_period: int | None = ..., giveaway_post_id: int | None = ..., stargift: TLObject | None = ..., floodskip_number: int | None = ..., starref_commission_permille: int | None = ..., starref_peer: TLObject | None = ..., starref_amount: TLObject | None = ..., paid_messages: int | None = ..., premium_gift_months: int | None = ..., ads_proceeds_from_date: int | None = ..., ads_proceeds_to_date: int | None = ...) -> None: ...

class starsTransactionPeer(TLObject):
    peer: TLObject
    def __init__(self, *, peer: TLObject) -> None: ...

class starsTransactionPeerAPI(TLObject):
    def __init__(self) -> None: ...

class starsTransactionPeerAds(TLObject):
    def __init__(self) -> None: ...

class starsTransactionPeerAppStore(TLObject):
    def __init__(self) -> None: ...

class starsTransactionPeerFragment(TLObject):
    def __init__(self) -> None: ...

class starsTransactionPeerPlayMarket(TLObject):
    def __init__(self) -> None: ...

class starsTransactionPeerPremiumBot(TLObject):
    def __init__(self) -> None: ...

class starsTransactionPeerUnsupported(TLObject):
    def __init__(self) -> None: ...

class stats:
    class broadcastStats(TLObject):
        period: TLObject
        followers: TLObject
        views_per_post: TLObject
        shares_per_post: TLObject
        reactions_per_post: TLObject
        views_per_story: TLObject
        shares_per_story: TLObject
        reactions_per_story: TLObject
        enabled_notifications: TLObject
        growth_graph: TLObject
        followers_graph: TLObject
        mute_graph: TLObject
        top_hours_graph: TLObject
        interactions_graph: TLObject
        iv_interactions_graph: TLObject
        views_by_source_graph: TLObject
        new_followers_by_source_graph: TLObject
        languages_graph: TLObject
        reactions_by_emotion_graph: TLObject
        story_interactions_graph: TLObject
        story_reactions_by_emotion_graph: TLObject
        recent_posts_interactions: list[TLObject]
        def __init__(self, *, period: TLObject, followers: TLObject, views_per_post: TLObject, shares_per_post: TLObject, reactions_per_post: TLObject, views_per_story: TLObject, shares_per_story: TLObject, reactions_per_story: TLObject, enabled_notifications: TLObject, growth_graph: TLObject, followers_graph: TLObject, mute_graph: TLObject, top_hours_graph: TLObject, interactions_graph: TLObject, iv_interactions_graph: TLObject, views_by_source_graph: TLObject, new_followers_by_source_graph: TLObject, languages_graph: TLObject, reactions_by_emotion_graph: TLObject, story_interactions_graph: TLObject, story_reactions_by_emotion_graph: TLObject, recent_posts_interactions: list[TLObject]) -> None: ...

    class getBroadcastStats(TLObject):
        dark: bool
        channel: TLObject
        def __init__(self, *, dark: bool = ..., channel: TLObject) -> None: ...

    class getMegagroupStats(TLObject):
        dark: bool
        channel: TLObject
        def __init__(self, *, dark: bool = ..., channel: TLObject) -> None: ...

    class getMessagePublicForwards(TLObject):
        channel: TLObject
        msg_id: int
        offset: str
        limit: int
        def __init__(self, *, channel: TLObject, msg_id: int, offset: str, limit: int) -> None: ...

    class getMessageStats(TLObject):
        dark: bool
        channel: TLObject
        msg_id: int
        def __init__(self, *, dark: bool = ..., channel: TLObject, msg_id: int) -> None: ...

    class getPollStats(TLObject):
        dark: bool
        peer: TLObject
        msg_id: int
        def __init__(self, *, dark: bool = ..., peer: TLObject, msg_id: int) -> None: ...

    class getStoryPublicForwards(TLObject):
        peer: TLObject
        id: int
        offset: str
        limit: int
        def __init__(self, *, peer: TLObject, id: int, offset: str, limit: int) -> None: ...

    class getStoryStats(TLObject):
        dark: bool
        peer: TLObject
        id: int
        def __init__(self, *, dark: bool = ..., peer: TLObject, id: int) -> None: ...

    class loadAsyncGraph(TLObject):
        token: str
        x: int | None
        def __init__(self, *, token: str, x: int | None = ...) -> None: ...

    class megagroupStats(TLObject):
        period: TLObject
        members: TLObject
        messages: TLObject
        viewers: TLObject
        posters: TLObject
        growth_graph: TLObject
        members_graph: TLObject
        new_members_by_source_graph: TLObject
        languages_graph: TLObject
        messages_graph: TLObject
        actions_graph: TLObject
        top_hours_graph: TLObject
        weekdays_graph: TLObject
        top_posters: list[TLObject]
        top_admins: list[TLObject]
        top_inviters: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, period: TLObject, members: TLObject, messages: TLObject, viewers: TLObject, posters: TLObject, growth_graph: TLObject, members_graph: TLObject, new_members_by_source_graph: TLObject, languages_graph: TLObject, messages_graph: TLObject, actions_graph: TLObject, top_hours_graph: TLObject, weekdays_graph: TLObject, top_posters: list[TLObject], top_admins: list[TLObject], top_inviters: list[TLObject], users: list[TLObject]) -> None: ...

    class messageStats(TLObject):
        views_graph: TLObject
        reactions_by_emotion_graph: TLObject
        def __init__(self, *, views_graph: TLObject, reactions_by_emotion_graph: TLObject) -> None: ...

    class pollStats(TLObject):
        votes_graph: TLObject
        def __init__(self, *, votes_graph: TLObject) -> None: ...

    class publicForwards(TLObject):
        count: int
        forwards: list[TLObject]
        next_offset: str | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, forwards: list[TLObject], next_offset: str | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class storyStats(TLObject):
        views_graph: TLObject
        reactions_by_emotion_graph: TLObject
        def __init__(self, *, views_graph: TLObject, reactions_by_emotion_graph: TLObject) -> None: ...

class statsAbsValueAndPrev(TLObject):
    current: float
    previous: float
    def __init__(self, *, current: float, previous: float) -> None: ...

class statsDateRangeDays(TLObject):
    min_date: int
    max_date: int
    def __init__(self, *, min_date: int, max_date: int) -> None: ...

class statsGraph(TLObject):
    json: TLObject
    zoom_token: str | None
    def __init__(self, *, json: TLObject, zoom_token: str | None = ...) -> None: ...

class statsGraphAsync(TLObject):
    token: str
    def __init__(self, *, token: str) -> None: ...

class statsGraphError(TLObject):
    error: str
    def __init__(self, *, error: str) -> None: ...

class statsGroupTopAdmin(TLObject):
    user_id: int
    deleted: int
    kicked: int
    banned: int
    def __init__(self, *, user_id: int, deleted: int, kicked: int, banned: int) -> None: ...

class statsGroupTopInviter(TLObject):
    user_id: int
    invitations: int
    def __init__(self, *, user_id: int, invitations: int) -> None: ...

class statsGroupTopPoster(TLObject):
    user_id: int
    messages: int
    avg_chars: int
    def __init__(self, *, user_id: int, messages: int, avg_chars: int) -> None: ...

class statsPercentValue(TLObject):
    part: float
    total: float
    def __init__(self, *, part: float, total: float) -> None: ...

class statsURL(TLObject):
    url: str
    def __init__(self, *, url: str) -> None: ...

class stickerKeyword(TLObject):
    document_id: int
    keyword: list[str]
    def __init__(self, *, document_id: int, keyword: list[str]) -> None: ...

class stickerPack(TLObject):
    emoticon: str
    documents: list[int]
    def __init__(self, *, emoticon: str, documents: list[int]) -> None: ...

class stickerSet(TLObject):
    archived: bool
    official: bool
    masks: bool
    emojis: bool
    text_color: bool
    channel_emoji_status: bool
    creator: bool
    installed_date: int | None
    id: int
    access_hash: int
    title: str
    short_name: str
    thumbs: list[TLObject] | None
    thumb_dc_id: int | None
    thumb_version: int | None
    thumb_document_id: int | None
    count: int
    hash: int
    def __init__(self, *, archived: bool = ..., official: bool = ..., masks: bool = ..., emojis: bool = ..., text_color: bool = ..., channel_emoji_status: bool = ..., creator: bool = ..., installed_date: int | None = ..., id: int, access_hash: int, title: str, short_name: str, thumbs: list[TLObject] | None = ..., thumb_dc_id: int | None = ..., thumb_version: int | None = ..., thumb_document_id: int | None = ..., count: int, hash: int) -> None: ...

class stickerSetCovered(TLObject):
    set: TLObject
    cover: TLObject
    def __init__(self, *, set: TLObject, cover: TLObject) -> None: ...

class stickerSetFullCovered(TLObject):
    set: TLObject
    packs: list[TLObject]
    keywords: list[TLObject]
    documents: list[TLObject]
    def __init__(self, *, set: TLObject, packs: list[TLObject], keywords: list[TLObject], documents: list[TLObject]) -> None: ...

class stickerSetMultiCovered(TLObject):
    set: TLObject
    covers: list[TLObject]
    def __init__(self, *, set: TLObject, covers: list[TLObject]) -> None: ...

class stickerSetNoCovered(TLObject):
    set: TLObject
    def __init__(self, *, set: TLObject) -> None: ...

class stickers:
    class addStickerToSet(TLObject):
        stickerset: TLObject
        sticker: TLObject
        def __init__(self, *, stickerset: TLObject, sticker: TLObject) -> None: ...

    class changeSticker(TLObject):
        sticker: TLObject
        emoji: str | None
        mask_coords: TLObject | None
        keywords: str | None
        def __init__(self, *, sticker: TLObject, emoji: str | None = ..., mask_coords: TLObject | None = ..., keywords: str | None = ...) -> None: ...

    class changeStickerPosition(TLObject):
        sticker: TLObject
        position: int
        def __init__(self, *, sticker: TLObject, position: int) -> None: ...

    class checkShortName(TLObject):
        short_name: str
        def __init__(self, *, short_name: str) -> None: ...

    class createStickerSet(TLObject):
        masks: bool
        emojis: bool
        text_color: bool
        user_id: TLObject
        title: str
        short_name: str
        thumb: TLObject | None
        stickers: list[TLObject]
        software: str | None
        def __init__(self, *, masks: bool = ..., emojis: bool = ..., text_color: bool = ..., user_id: TLObject, title: str, short_name: str, thumb: TLObject | None = ..., stickers: list[TLObject], software: str | None = ...) -> None: ...

    class deleteStickerSet(TLObject):
        stickerset: TLObject
        def __init__(self, *, stickerset: TLObject) -> None: ...

    class removeStickerFromSet(TLObject):
        sticker: TLObject
        def __init__(self, *, sticker: TLObject) -> None: ...

    class renameStickerSet(TLObject):
        stickerset: TLObject
        title: str
        def __init__(self, *, stickerset: TLObject, title: str) -> None: ...

    class replaceSticker(TLObject):
        sticker: TLObject
        new_sticker: TLObject
        def __init__(self, *, sticker: TLObject, new_sticker: TLObject) -> None: ...

    class setStickerSetThumb(TLObject):
        stickerset: TLObject
        thumb: TLObject | None
        thumb_document_id: int | None
        def __init__(self, *, stickerset: TLObject, thumb: TLObject | None = ..., thumb_document_id: int | None = ...) -> None: ...

    class suggestShortName(TLObject):
        title: str
        def __init__(self, *, title: str) -> None: ...

    class suggestedShortName(TLObject):
        short_name: str
        def __init__(self, *, short_name: str) -> None: ...

class storage:
    class fileGif(TLObject):
        def __init__(self) -> None: ...

    class fileJpeg(TLObject):
        def __init__(self) -> None: ...

    class fileMov(TLObject):
        def __init__(self) -> None: ...

    class fileMp3(TLObject):
        def __init__(self) -> None: ...

    class fileMp4(TLObject):
        def __init__(self) -> None: ...

    class filePartial(TLObject):
        def __init__(self) -> None: ...

    class filePdf(TLObject):
        def __init__(self) -> None: ...

    class filePng(TLObject):
        def __init__(self) -> None: ...

    class fileUnknown(TLObject):
        def __init__(self) -> None: ...

    class fileWebp(TLObject):
        def __init__(self) -> None: ...

class stories:
    class activateStealthMode(TLObject):
        past: bool
        future: bool
        def __init__(self, *, past: bool = ..., future: bool = ...) -> None: ...

    class albums(TLObject):
        hash: int
        albums: list[TLObject]
        def __init__(self, *, hash: int, albums: list[TLObject]) -> None: ...

    class albumsNotModified(TLObject):
        def __init__(self) -> None: ...

    class allStories(TLObject):
        has_more: bool
        count: int
        state: str
        peer_stories: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        stealth_mode: TLObject
        def __init__(self, *, has_more: bool = ..., count: int, state: str, peer_stories: list[TLObject], chats: list[TLObject], users: list[TLObject], stealth_mode: TLObject) -> None: ...

    class allStoriesNotModified(TLObject):
        state: str
        stealth_mode: TLObject
        def __init__(self, *, state: str, stealth_mode: TLObject) -> None: ...

    class canSendStory(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class canSendStoryCount(TLObject):
        count_remains: int
        def __init__(self, *, count_remains: int) -> None: ...

    class createAlbum(TLObject):
        peer: TLObject
        title: str
        stories: list[int]
        def __init__(self, *, peer: TLObject, title: str, stories: list[int]) -> None: ...

    class deleteAlbum(TLObject):
        peer: TLObject
        album_id: int
        def __init__(self, *, peer: TLObject, album_id: int) -> None: ...

    class deleteStories(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class editStory(TLObject):
        peer: TLObject
        id: int
        media: TLObject | None
        media_areas: list[TLObject] | None
        caption: str | None
        entities: list[TLObject] | None
        privacy_rules: list[TLObject] | None
        music: TLObject | None
        def __init__(self, *, peer: TLObject, id: int, media: TLObject | None = ..., media_areas: list[TLObject] | None = ..., caption: str | None = ..., entities: list[TLObject] | None = ..., privacy_rules: list[TLObject] | None = ..., music: TLObject | None = ...) -> None: ...

    class exportStoryLink(TLObject):
        peer: TLObject
        id: int
        def __init__(self, *, peer: TLObject, id: int) -> None: ...

    class foundStories(TLObject):
        count: int
        stories: list[TLObject]
        next_offset: str | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, stories: list[TLObject], next_offset: str | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class getAlbumStories(TLObject):
        peer: TLObject
        album_id: int
        offset: int
        limit: int
        def __init__(self, *, peer: TLObject, album_id: int, offset: int, limit: int) -> None: ...

    class getAlbums(TLObject):
        peer: TLObject
        hash: int
        def __init__(self, *, peer: TLObject, hash: int) -> None: ...

    class getAllReadPeerStories(TLObject):
        def __init__(self) -> None: ...

    class getAllStories(TLObject):
        next: bool
        hidden: bool
        state: str | None
        def __init__(self, *, next: bool = ..., hidden: bool = ..., state: str | None = ...) -> None: ...

    class getChatsToSend(TLObject):
        def __init__(self) -> None: ...

    class getPeerMaxIDs(TLObject):
        id: list[TLObject]
        def __init__(self, *, id: list[TLObject]) -> None: ...

    class getPeerStories(TLObject):
        peer: TLObject
        def __init__(self, *, peer: TLObject) -> None: ...

    class getPinnedStories(TLObject):
        peer: TLObject
        offset_id: int
        limit: int
        def __init__(self, *, peer: TLObject, offset_id: int, limit: int) -> None: ...

    class getStoriesArchive(TLObject):
        peer: TLObject
        offset_id: int
        limit: int
        def __init__(self, *, peer: TLObject, offset_id: int, limit: int) -> None: ...

    class getStoriesByID(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class getStoriesViews(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class getStoryReactionsList(TLObject):
        forwards_first: bool
        peer: TLObject
        id: int
        reaction: TLObject | None
        offset: str | None
        limit: int
        def __init__(self, *, forwards_first: bool = ..., peer: TLObject, id: int, reaction: TLObject | None = ..., offset: str | None = ..., limit: int) -> None: ...

    class getStoryViewsList(TLObject):
        just_contacts: bool
        reactions_first: bool
        forwards_first: bool
        peer: TLObject
        q: str | None
        id: int
        offset: str
        limit: int
        def __init__(self, *, just_contacts: bool = ..., reactions_first: bool = ..., forwards_first: bool = ..., peer: TLObject, q: str | None = ..., id: int, offset: str, limit: int) -> None: ...

    class incrementStoryViews(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class peerStories(TLObject):
        stories: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, stories: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class readStories(TLObject):
        peer: TLObject
        max_id: int
        def __init__(self, *, peer: TLObject, max_id: int) -> None: ...

    class reorderAlbums(TLObject):
        peer: TLObject
        order: list[int]
        def __init__(self, *, peer: TLObject, order: list[int]) -> None: ...

    class report(TLObject):
        peer: TLObject
        id: list[int]
        option: bytes
        message: str
        def __init__(self, *, peer: TLObject, id: list[int], option: bytes, message: str) -> None: ...

    class searchPosts(TLObject):
        hashtag: str | None
        area: TLObject | None
        peer: TLObject | None
        offset: str
        limit: int
        def __init__(self, *, hashtag: str | None = ..., area: TLObject | None = ..., peer: TLObject | None = ..., offset: str, limit: int) -> None: ...

    class sendReaction(TLObject):
        add_to_recent: bool
        peer: TLObject
        story_id: int
        reaction: TLObject
        def __init__(self, *, add_to_recent: bool = ..., peer: TLObject, story_id: int, reaction: TLObject) -> None: ...

    class sendStory(TLObject):
        pinned: bool
        noforwards: bool
        fwd_modified: bool
        peer: TLObject
        media: TLObject
        media_areas: list[TLObject] | None
        caption: str | None
        entities: list[TLObject] | None
        privacy_rules: list[TLObject]
        random_id: int
        period: int | None
        fwd_from_id: TLObject | None
        fwd_from_story: int | None
        albums: list[int] | None
        music: TLObject | None
        def __init__(self, *, pinned: bool = ..., noforwards: bool = ..., fwd_modified: bool = ..., peer: TLObject, media: TLObject, media_areas: list[TLObject] | None = ..., caption: str | None = ..., entities: list[TLObject] | None = ..., privacy_rules: list[TLObject], random_id: int, period: int | None = ..., fwd_from_id: TLObject | None = ..., fwd_from_story: int | None = ..., albums: list[int] | None = ..., music: TLObject | None = ...) -> None: ...

    class startLive(TLObject):
        pinned: bool
        noforwards: bool
        rtmp_stream: bool
        peer: TLObject
        caption: str | None
        entities: list[TLObject] | None
        privacy_rules: list[TLObject]
        random_id: int
        messages_enabled: bool
        send_paid_messages_stars: int | None
        def __init__(self, *, pinned: bool = ..., noforwards: bool = ..., rtmp_stream: bool = ..., peer: TLObject, caption: str | None = ..., entities: list[TLObject] | None = ..., privacy_rules: list[TLObject], random_id: int, messages_enabled: bool = ..., send_paid_messages_stars: int | None = ...) -> None: ...

    class stories(TLObject):
        count: int
        stories: list[TLObject]
        pinned_to_top: list[int] | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, count: int, stories: list[TLObject], pinned_to_top: list[int] | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class storyReactionsList(TLObject):
        count: int
        reactions: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        next_offset: str | None
        def __init__(self, *, count: int, reactions: list[TLObject], chats: list[TLObject], users: list[TLObject], next_offset: str | None = ...) -> None: ...

    class storyViews(TLObject):
        views: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, views: list[TLObject], users: list[TLObject]) -> None: ...

    class storyViewsList(TLObject):
        count: int
        views_count: int
        forwards_count: int
        reactions_count: int
        views: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        next_offset: str | None
        def __init__(self, *, count: int, views_count: int, forwards_count: int, reactions_count: int, views: list[TLObject], chats: list[TLObject], users: list[TLObject], next_offset: str | None = ...) -> None: ...

    class toggleAllStoriesHidden(TLObject):
        hidden: bool
        def __init__(self, *, hidden: bool) -> None: ...

    class togglePeerStoriesHidden(TLObject):
        peer: TLObject
        hidden: bool
        def __init__(self, *, peer: TLObject, hidden: bool) -> None: ...

    class togglePinned(TLObject):
        peer: TLObject
        id: list[int]
        pinned: bool
        def __init__(self, *, peer: TLObject, id: list[int], pinned: bool) -> None: ...

    class togglePinnedToTop(TLObject):
        peer: TLObject
        id: list[int]
        def __init__(self, *, peer: TLObject, id: list[int]) -> None: ...

    class updateAlbum(TLObject):
        peer: TLObject
        album_id: int
        title: str | None
        delete_stories: list[int] | None
        add_stories: list[int] | None
        order: list[int] | None
        def __init__(self, *, peer: TLObject, album_id: int, title: str | None = ..., delete_stories: list[int] | None = ..., add_stories: list[int] | None = ..., order: list[int] | None = ...) -> None: ...

class storiesStealthMode(TLObject):
    active_until_date: int | None
    cooldown_until_date: int | None
    def __init__(self, *, active_until_date: int | None = ..., cooldown_until_date: int | None = ...) -> None: ...

class storyAlbum(TLObject):
    album_id: int
    title: str
    icon_photo: TLObject | None
    icon_video: TLObject | None
    def __init__(self, *, album_id: int, title: str, icon_photo: TLObject | None = ..., icon_video: TLObject | None = ...) -> None: ...

class storyFwdHeader(TLObject):
    modified: bool
    from_: TLObject | None
    from_name: str | None
    story_id: int | None
    def __init__(self, *, modified: bool = ..., from_: TLObject | None = ..., from_name: str | None = ..., story_id: int | None = ...) -> None: ...

class storyItem(TLObject):
    pinned: bool
    public: bool
    close_friends: bool
    min: bool
    noforwards: bool
    edited: bool
    contacts: bool
    selected_contacts: bool
    out: bool
    id: int
    date: int
    from_id: TLObject | None
    fwd_from: TLObject | None
    expire_date: int
    caption: str | None
    entities: list[TLObject] | None
    media: TLObject
    media_areas: list[TLObject] | None
    privacy: list[TLObject] | None
    views: TLObject | None
    sent_reaction: TLObject | None
    albums: list[int] | None
    music: TLObject | None
    def __init__(self, *, pinned: bool = ..., public: bool = ..., close_friends: bool = ..., min: bool = ..., noforwards: bool = ..., edited: bool = ..., contacts: bool = ..., selected_contacts: bool = ..., out: bool = ..., id: int, date: int, from_id: TLObject | None = ..., fwd_from: TLObject | None = ..., expire_date: int, caption: str | None = ..., entities: list[TLObject] | None = ..., media: TLObject, media_areas: list[TLObject] | None = ..., privacy: list[TLObject] | None = ..., views: TLObject | None = ..., sent_reaction: TLObject | None = ..., albums: list[int] | None = ..., music: TLObject | None = ...) -> None: ...

class storyItemDeleted(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class storyItemSkipped(TLObject):
    close_friends: bool
    live: bool
    id: int
    date: int
    expire_date: int
    def __init__(self, *, close_friends: bool = ..., live: bool = ..., id: int, date: int, expire_date: int) -> None: ...

class storyReaction(TLObject):
    peer_id: TLObject
    date: int
    reaction: TLObject
    def __init__(self, *, peer_id: TLObject, date: int, reaction: TLObject) -> None: ...

class storyReactionPublicForward(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class storyReactionPublicRepost(TLObject):
    peer_id: TLObject
    story: TLObject
    def __init__(self, *, peer_id: TLObject, story: TLObject) -> None: ...

class storyView(TLObject):
    blocked: bool
    blocked_my_stories_from: bool
    user_id: int
    date: int
    reaction: TLObject | None
    def __init__(self, *, blocked: bool = ..., blocked_my_stories_from: bool = ..., user_id: int, date: int, reaction: TLObject | None = ...) -> None: ...

class storyViewPublicForward(TLObject):
    blocked: bool
    blocked_my_stories_from: bool
    message: TLObject
    def __init__(self, *, blocked: bool = ..., blocked_my_stories_from: bool = ..., message: TLObject) -> None: ...

class storyViewPublicRepost(TLObject):
    blocked: bool
    blocked_my_stories_from: bool
    peer_id: TLObject
    story: TLObject
    def __init__(self, *, blocked: bool = ..., blocked_my_stories_from: bool = ..., peer_id: TLObject, story: TLObject) -> None: ...

class storyViews(TLObject):
    has_viewers: bool
    views_count: int
    forwards_count: int | None
    reactions: list[TLObject] | None
    reactions_count: int | None
    recent_viewers: list[int] | None
    def __init__(self, *, has_viewers: bool = ..., views_count: int, forwards_count: int | None = ..., reactions: list[TLObject] | None = ..., reactions_count: int | None = ..., recent_viewers: list[int] | None = ...) -> None: ...

class suggestedPost(TLObject):
    accepted: bool
    rejected: bool
    price: TLObject | None
    schedule_date: int | None
    def __init__(self, *, accepted: bool = ..., rejected: bool = ..., price: TLObject | None = ..., schedule_date: int | None = ...) -> None: ...

class textAnchor(TLObject):
    text: TLObject
    name: str
    def __init__(self, *, text: TLObject, name: str) -> None: ...

class textAutoEmail(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textAutoPhone(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textAutoUrl(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textBankCard(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textBold(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textBotCommand(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textButton(TLObject):
    text: TLObject
    type: TLObject
    style: TLObject | None
    def __init__(self, *, text: TLObject, type: TLObject, style: TLObject | None = ...) -> None: ...

class textCashtag(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textConcat(TLObject):
    texts: list[TLObject]
    def __init__(self, *, texts: list[TLObject]) -> None: ...

class textCustomEmoji(TLObject):
    document_id: int
    alt: str
    def __init__(self, *, document_id: int, alt: str) -> None: ...

class textDate(TLObject):
    relative: bool
    short_time: bool
    long_time: bool
    short_date: bool
    long_date: bool
    day_of_week: bool
    text: TLObject
    date: int
    def __init__(self, *, relative: bool = ..., short_time: bool = ..., long_time: bool = ..., short_date: bool = ..., long_date: bool = ..., day_of_week: bool = ..., text: TLObject, date: int) -> None: ...

class textDiff(TLObject):
    text: TLObject
    old_text: TLObject
    def __init__(self, *, text: TLObject, old_text: TLObject) -> None: ...

class textEmail(TLObject):
    text: TLObject
    email: str
    def __init__(self, *, text: TLObject, email: str) -> None: ...

class textEmpty(TLObject):
    def __init__(self) -> None: ...

class textFixed(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textHashtag(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textImage(TLObject):
    document_id: int
    w: int
    h: int
    def __init__(self, *, document_id: int, w: int, h: int) -> None: ...

class textItalic(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textMarked(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textMath(TLObject):
    source: str
    def __init__(self, *, source: str) -> None: ...

class textMention(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textMentionName(TLObject):
    text: TLObject
    user_id: int
    def __init__(self, *, text: TLObject, user_id: int) -> None: ...

class textPhone(TLObject):
    text: TLObject
    phone: str
    def __init__(self, *, text: TLObject, phone: str) -> None: ...

class textPlain(TLObject):
    text: str
    def __init__(self, *, text: str) -> None: ...

class textSpoiler(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textStrike(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textSubscript(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textSuperscript(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textTonAddress(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textUnderline(TLObject):
    text: TLObject
    def __init__(self, *, text: TLObject) -> None: ...

class textUrl(TLObject):
    text: TLObject
    url: str
    webpage_id: int
    def __init__(self, *, text: TLObject, url: str, webpage_id: int) -> None: ...

class textWithEntities(TLObject):
    text: str
    entities: list[TLObject]
    def __init__(self, *, text: str, entities: list[TLObject]) -> None: ...

class theme(TLObject):
    creator: bool
    default: bool
    for_chat: bool
    id: int
    access_hash: int
    slug: str
    title: str
    document: TLObject | None
    settings: list[TLObject] | None
    emoticon: str | None
    installs_count: int | None
    def __init__(self, *, creator: bool = ..., default: bool = ..., for_chat: bool = ..., id: int, access_hash: int, slug: str, title: str, document: TLObject | None = ..., settings: list[TLObject] | None = ..., emoticon: str | None = ..., installs_count: int | None = ...) -> None: ...

class themeSettings(TLObject):
    message_colors_animated: bool
    base_theme: TLObject
    accent_color: int
    outbox_accent_color: int | None
    message_colors: list[int] | None
    wallpaper: TLObject | None
    def __init__(self, *, message_colors_animated: bool = ..., base_theme: TLObject, accent_color: int, outbox_accent_color: int | None = ..., message_colors: list[int] | None = ..., wallpaper: TLObject | None = ...) -> None: ...

class timezone(TLObject):
    id: str
    name: str
    utc_offset: int
    def __init__(self, *, id: str, name: str, utc_offset: int) -> None: ...

class todoCompletion(TLObject):
    id: int
    completed_by: TLObject
    date: int
    def __init__(self, *, id: int, completed_by: TLObject, date: int) -> None: ...

class todoItem(TLObject):
    id: int
    title: TLObject
    def __init__(self, *, id: int, title: TLObject) -> None: ...

class todoList(TLObject):
    others_can_append: bool
    others_can_complete: bool
    title: TLObject
    list: list[TLObject]
    def __init__(self, *, others_can_append: bool = ..., others_can_complete: bool = ..., title: TLObject, list: list[TLObject]) -> None: ...

class tonConnectManifest(TLObject):
    url: str
    name: str
    icon: TLObject | None
    def __init__(self, *, url: str, name: str, icon: TLObject | None = ...) -> None: ...

class tonConnectNextEventId(TLObject):
    event_id: int
    def __init__(self, *, event_id: int) -> None: ...

class tonConnectRequest(TLObject):
    session_id: int
    msg_id: int
    body: bytes
    expires: int
    topic: str | None
    trace_id: str | None
    def __init__(self, *, session_id: int, msg_id: int, body: bytes, expires: int, topic: str | None = ..., trace_id: str | None = ...) -> None: ...

class tonConnectSession(TLObject):
    pending: bool
    closing: bool
    closed: bool
    id: int
    dapp_client_id: str
    client_id: str | None
    nonce: bytes
    manifest: TLObject | None
    manifest_error: int | None
    date: int
    def __init__(self, *, pending: bool = ..., closing: bool = ..., closed: bool = ..., id: int, dapp_client_id: str, client_id: str | None = ..., nonce: bytes, manifest: TLObject | None = ..., manifest_error: int | None = ..., date: int) -> None: ...

class toncenter:
    class apiResponse(TLObject):
        response: TLObject
        def __init__(self, *, response: TLObject) -> None: ...

    class getStreamingUrl(TLObject):
        def __init__(self) -> None: ...

    class performApiRequest(TLObject):
        post: bool
        endpoint: str
        query: str | None
        payload: str | None
        def __init__(self, *, post: bool = ..., endpoint: str, query: str | None = ..., payload: str | None = ...) -> None: ...

    class streamingUrl(TLObject):
        url: str
        expires: int
        def __init__(self, *, url: str, expires: int) -> None: ...

class topPeer(TLObject):
    peer: TLObject
    rating: float
    def __init__(self, *, peer: TLObject, rating: float) -> None: ...

class topPeerCategoryBotsApp(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryBotsGuestChat(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryBotsInline(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryBotsPM(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryChannels(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryCorrespondents(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryForwardChats(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryForwardUsers(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryGroups(TLObject):
    def __init__(self) -> None: ...

class topPeerCategoryPeers(TLObject):
    category: TLObject
    count: int
    peers: list[TLObject]
    def __init__(self, *, category: TLObject, count: int, peers: list[TLObject]) -> None: ...

class topPeerCategoryPhoneCalls(TLObject):
    def __init__(self) -> None: ...

class true(TLObject):
    def __init__(self) -> None: ...

class updateAiComposeTones(TLObject):
    def __init__(self) -> None: ...

class updateAttachMenuBots(TLObject):
    def __init__(self) -> None: ...

class updateAutoSaveSettings(TLObject):
    def __init__(self) -> None: ...

class updateBotBusinessConnect(TLObject):
    connection: TLObject
    qts: int
    def __init__(self, *, connection: TLObject, qts: int) -> None: ...

class updateBotCallbackQuery(TLObject):
    query_id: int
    user_id: int
    peer: TLObject
    msg_id: int
    chat_instance: int
    data: bytes | None
    game_short_name: str | None
    def __init__(self, *, query_id: int, user_id: int, peer: TLObject, msg_id: int, chat_instance: int, data: bytes | None = ..., game_short_name: str | None = ...) -> None: ...

class updateBotChatBoost(TLObject):
    peer: TLObject
    boost: TLObject
    qts: int
    def __init__(self, *, peer: TLObject, boost: TLObject, qts: int) -> None: ...

class updateBotChatInviteRequester(TLObject):
    peer: TLObject
    date: int
    user_id: int
    about: str
    invite: TLObject
    qts: int
    query_id: int | None
    def __init__(self, *, peer: TLObject, date: int, user_id: int, about: str, invite: TLObject, qts: int, query_id: int | None = ...) -> None: ...

class updateBotCommands(TLObject):
    peer: TLObject
    bot_id: int
    commands: list[TLObject]
    def __init__(self, *, peer: TLObject, bot_id: int, commands: list[TLObject]) -> None: ...

class updateBotDeleteBusinessMessage(TLObject):
    connection_id: str
    peer: TLObject
    messages: list[int]
    qts: int
    def __init__(self, *, connection_id: str, peer: TLObject, messages: list[int], qts: int) -> None: ...

class updateBotEditBusinessMessage(TLObject):
    connection_id: str
    message: TLObject
    reply_to_message: TLObject | None
    qts: int
    def __init__(self, *, connection_id: str, message: TLObject, reply_to_message: TLObject | None = ..., qts: int) -> None: ...

class updateBotGuestChatQuery(TLObject):
    query_id: int
    message: TLObject
    reference_messages: list[TLObject] | None
    qts: int
    def __init__(self, *, query_id: int, message: TLObject, reference_messages: list[TLObject] | None = ..., qts: int) -> None: ...

class updateBotInlineQuery(TLObject):
    query_id: int
    user_id: int
    query: str
    geo: TLObject | None
    peer_type: TLObject | None
    offset: str
    def __init__(self, *, query_id: int, user_id: int, query: str, geo: TLObject | None = ..., peer_type: TLObject | None = ..., offset: str) -> None: ...

class updateBotInlineSend(TLObject):
    user_id: int
    query: str
    geo: TLObject | None
    id: str
    msg_id: TLObject | None
    def __init__(self, *, user_id: int, query: str, geo: TLObject | None = ..., id: str, msg_id: TLObject | None = ...) -> None: ...

class updateBotMenuButton(TLObject):
    bot_id: int
    button: TLObject
    def __init__(self, *, bot_id: int, button: TLObject) -> None: ...

class updateBotMessageReaction(TLObject):
    peer: TLObject
    msg_id: int
    date: int
    actor: TLObject
    old_reactions: list[TLObject]
    new_reactions: list[TLObject]
    qts: int
    def __init__(self, *, peer: TLObject, msg_id: int, date: int, actor: TLObject, old_reactions: list[TLObject], new_reactions: list[TLObject], qts: int) -> None: ...

class updateBotMessageReactions(TLObject):
    peer: TLObject
    msg_id: int
    date: int
    reactions: list[TLObject]
    qts: int
    def __init__(self, *, peer: TLObject, msg_id: int, date: int, reactions: list[TLObject], qts: int) -> None: ...

class updateBotNewBusinessMessage(TLObject):
    connection_id: str
    message: TLObject
    reply_to_message: TLObject | None
    qts: int
    def __init__(self, *, connection_id: str, message: TLObject, reply_to_message: TLObject | None = ..., qts: int) -> None: ...

class updateBotPrecheckoutQuery(TLObject):
    query_id: int
    user_id: int
    payload: bytes
    info: TLObject | None
    shipping_option_id: str | None
    currency: str
    total_amount: int
    def __init__(self, *, query_id: int, user_id: int, payload: bytes, info: TLObject | None = ..., shipping_option_id: str | None = ..., currency: str, total_amount: int) -> None: ...

class updateBotPurchasedPaidMedia(TLObject):
    user_id: int
    payload: str
    qts: int
    def __init__(self, *, user_id: int, payload: str, qts: int) -> None: ...

class updateBotShippingQuery(TLObject):
    query_id: int
    user_id: int
    payload: bytes
    shipping_address: TLObject
    def __init__(self, *, query_id: int, user_id: int, payload: bytes, shipping_address: TLObject) -> None: ...

class updateBotStarsSubscription(TLObject):
    canceled: bool
    payment_failed: bool
    restored: bool
    user_id: int
    payload: bytes
    qts: int
    def __init__(self, *, canceled: bool = ..., payment_failed: bool = ..., restored: bool = ..., user_id: int, payload: bytes, qts: int) -> None: ...

class updateBotStopped(TLObject):
    user_id: int
    date: int
    stopped: bool
    qts: int
    def __init__(self, *, user_id: int, date: int, stopped: bool, qts: int) -> None: ...

class updateBotWebhookJSON(TLObject):
    data: TLObject
    def __init__(self, *, data: TLObject) -> None: ...

class updateBotWebhookJSONQuery(TLObject):
    query_id: int
    data: TLObject
    timeout: int
    def __init__(self, *, query_id: int, data: TLObject, timeout: int) -> None: ...

class updateBotWidgetCopyQuery(TLObject):
    query_id: int
    query_type: TLObject
    user_id: int
    data: bytes
    widget_id: int
    wallet_card: TLObject | None
    def __init__(self, *, query_id: int, query_type: TLObject, user_id: int, data: bytes, widget_id: int, wallet_card: TLObject | None = ...) -> None: ...

class updateBotWidgetQuery(TLObject):
    query_id: int
    query_type: TLObject
    user_id: int
    peer: TLObject
    msg_id: int
    chat_instance: int
    chat_type: str
    data: bytes
    widget_id: int | None
    wallet_card: TLObject | None
    def __init__(self, *, query_id: int, query_type: TLObject, user_id: int, peer: TLObject, msg_id: int, chat_instance: int, chat_type: str, data: bytes, widget_id: int | None = ..., wallet_card: TLObject | None = ...) -> None: ...

class updateBusinessBotCallbackQuery(TLObject):
    query_id: int
    user_id: int
    connection_id: str
    message: TLObject
    reply_to_message: TLObject | None
    chat_instance: int
    data: bytes | None
    def __init__(self, *, query_id: int, user_id: int, connection_id: str, message: TLObject, reply_to_message: TLObject | None = ..., chat_instance: int, data: bytes | None = ...) -> None: ...

class updateChannel(TLObject):
    channel_id: int
    def __init__(self, *, channel_id: int) -> None: ...

class updateChannelAvailableMessages(TLObject):
    channel_id: int
    available_min_id: int
    def __init__(self, *, channel_id: int, available_min_id: int) -> None: ...

class updateChannelMessageForwards(TLObject):
    channel_id: int
    id: int
    forwards: int
    def __init__(self, *, channel_id: int, id: int, forwards: int) -> None: ...

class updateChannelMessageViews(TLObject):
    channel_id: int
    id: int
    views: int
    def __init__(self, *, channel_id: int, id: int, views: int) -> None: ...

class updateChannelParticipant(TLObject):
    via_chatlist: bool
    channel_id: int
    date: int
    actor_id: int
    user_id: int
    prev_participant: TLObject | None
    new_participant: TLObject | None
    invite: TLObject | None
    qts: int
    def __init__(self, *, via_chatlist: bool = ..., channel_id: int, date: int, actor_id: int, user_id: int, prev_participant: TLObject | None = ..., new_participant: TLObject | None = ..., invite: TLObject | None = ..., qts: int) -> None: ...

class updateChannelReadMessagesContents(TLObject):
    channel_id: int
    top_msg_id: int | None
    saved_peer_id: TLObject | None
    messages: list[int]
    def __init__(self, *, channel_id: int, top_msg_id: int | None = ..., saved_peer_id: TLObject | None = ..., messages: list[int]) -> None: ...

class updateChannelTooLong(TLObject):
    channel_id: int
    pts: int | None
    def __init__(self, *, channel_id: int, pts: int | None = ...) -> None: ...

class updateChannelUserTyping(TLObject):
    channel_id: int
    top_msg_id: int | None
    from_id: TLObject
    action: TLObject
    def __init__(self, *, channel_id: int, top_msg_id: int | None = ..., from_id: TLObject, action: TLObject) -> None: ...

class updateChannelViewForumAsMessages(TLObject):
    channel_id: int
    enabled: bool
    def __init__(self, *, channel_id: int, enabled: bool) -> None: ...

class updateChannelWebPage(TLObject):
    channel_id: int
    webpage: TLObject
    pts: int
    pts_count: int
    def __init__(self, *, channel_id: int, webpage: TLObject, pts: int, pts_count: int) -> None: ...

class updateChat(TLObject):
    chat_id: int
    def __init__(self, *, chat_id: int) -> None: ...

class updateChatDefaultBannedRights(TLObject):
    peer: TLObject
    default_banned_rights: TLObject
    version: int
    def __init__(self, *, peer: TLObject, default_banned_rights: TLObject, version: int) -> None: ...

class updateChatParticipant(TLObject):
    chat_id: int
    date: int
    actor_id: int
    user_id: int
    prev_participant: TLObject | None
    new_participant: TLObject | None
    invite: TLObject | None
    qts: int
    def __init__(self, *, chat_id: int, date: int, actor_id: int, user_id: int, prev_participant: TLObject | None = ..., new_participant: TLObject | None = ..., invite: TLObject | None = ..., qts: int) -> None: ...

class updateChatParticipantAdd(TLObject):
    chat_id: int
    user_id: int
    inviter_id: int
    date: int
    version: int
    def __init__(self, *, chat_id: int, user_id: int, inviter_id: int, date: int, version: int) -> None: ...

class updateChatParticipantAdmin(TLObject):
    chat_id: int
    user_id: int
    is_admin: bool
    version: int
    def __init__(self, *, chat_id: int, user_id: int, is_admin: bool, version: int) -> None: ...

class updateChatParticipantDelete(TLObject):
    chat_id: int
    user_id: int
    version: int
    def __init__(self, *, chat_id: int, user_id: int, version: int) -> None: ...

class updateChatParticipantRank(TLObject):
    chat_id: int
    user_id: int
    rank: str
    version: int
    def __init__(self, *, chat_id: int, user_id: int, rank: str, version: int) -> None: ...

class updateChatParticipants(TLObject):
    participants: TLObject
    def __init__(self, *, participants: TLObject) -> None: ...

class updateChatUserTyping(TLObject):
    chat_id: int
    from_id: TLObject
    action: TLObject
    def __init__(self, *, chat_id: int, from_id: TLObject, action: TLObject) -> None: ...

class updateConfig(TLObject):
    def __init__(self) -> None: ...

class updateContactsReset(TLObject):
    def __init__(self) -> None: ...

class updateDcOptions(TLObject):
    dc_options: list[TLObject]
    def __init__(self, *, dc_options: list[TLObject]) -> None: ...

class updateDeleteChannelMessages(TLObject):
    channel_id: int
    messages: list[int]
    pts: int
    pts_count: int
    def __init__(self, *, channel_id: int, messages: list[int], pts: int, pts_count: int) -> None: ...

class updateDeleteEphemeralMessages(TLObject):
    peer: TLObject
    ids: list[int]
    def __init__(self, *, peer: TLObject, ids: list[int]) -> None: ...

class updateDeleteGroupCallMessages(TLObject):
    call: TLObject
    messages: list[int]
    def __init__(self, *, call: TLObject, messages: list[int]) -> None: ...

class updateDeleteMessages(TLObject):
    messages: list[int]
    pts: int
    pts_count: int
    def __init__(self, *, messages: list[int], pts: int, pts_count: int) -> None: ...

class updateDeleteQuickReply(TLObject):
    shortcut_id: int
    def __init__(self, *, shortcut_id: int) -> None: ...

class updateDeleteQuickReplyMessages(TLObject):
    shortcut_id: int
    messages: list[int]
    def __init__(self, *, shortcut_id: int, messages: list[int]) -> None: ...

class updateDeleteScheduledMessages(TLObject):
    peer: TLObject
    messages: list[int]
    sent_messages: list[int] | None
    def __init__(self, *, peer: TLObject, messages: list[int], sent_messages: list[int] | None = ...) -> None: ...

class updateDialogFilter(TLObject):
    id: int
    filter: TLObject | None
    def __init__(self, *, id: int, filter: TLObject | None = ...) -> None: ...

class updateDialogFilterOrder(TLObject):
    order: list[int]
    def __init__(self, *, order: list[int]) -> None: ...

class updateDialogFilters(TLObject):
    def __init__(self) -> None: ...

class updateDialogPinned(TLObject):
    pinned: bool
    folder_id: int | None
    peer: TLObject
    def __init__(self, *, pinned: bool = ..., folder_id: int | None = ..., peer: TLObject) -> None: ...

class updateDialogUnreadMark(TLObject):
    unread: bool
    peer: TLObject
    saved_peer_id: TLObject | None
    def __init__(self, *, unread: bool = ..., peer: TLObject, saved_peer_id: TLObject | None = ...) -> None: ...

class updateDraftMessage(TLObject):
    peer: TLObject
    top_msg_id: int | None
    saved_peer_id: TLObject | None
    draft: TLObject
    def __init__(self, *, peer: TLObject, top_msg_id: int | None = ..., saved_peer_id: TLObject | None = ..., draft: TLObject) -> None: ...

class updateEditChannelMessage(TLObject):
    message: TLObject
    pts: int
    pts_count: int
    def __init__(self, *, message: TLObject, pts: int, pts_count: int) -> None: ...

class updateEditEphemeralMessage(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class updateEditForumTopic(TLObject):
    peer: TLObject
    topic_id: int
    title: str | None
    icon_emoji_id: int | None
    closed: bool
    hidden: bool
    def __init__(self, *, peer: TLObject, topic_id: int, title: str | None = ..., icon_emoji_id: int | None = ..., closed: bool = ..., hidden: bool = ...) -> None: ...

class updateEditMessage(TLObject):
    message: TLObject
    pts: int
    pts_count: int
    def __init__(self, *, message: TLObject, pts: int, pts_count: int) -> None: ...

class updateEmojiGameInfo(TLObject):
    info: TLObject
    def __init__(self, *, info: TLObject) -> None: ...

class updateEncryptedChatTyping(TLObject):
    chat_id: int
    def __init__(self, *, chat_id: int) -> None: ...

class updateEncryptedMessagesRead(TLObject):
    chat_id: int
    max_date: int
    date: int
    def __init__(self, *, chat_id: int, max_date: int, date: int) -> None: ...

class updateEncryption(TLObject):
    chat: TLObject
    date: int
    def __init__(self, *, chat: TLObject, date: int) -> None: ...

class updateEphemeralBotCallbackQuery(TLObject):
    query_id: int
    user_id: int
    peer: TLObject | None
    msg_id: int
    data: bytes
    chat_instance: int | None
    message: TLObject
    def __init__(self, *, query_id: int, user_id: int, peer: TLObject | None = ..., msg_id: int, data: bytes, chat_instance: int | None = ..., message: TLObject) -> None: ...

class updateFavedStickers(TLObject):
    def __init__(self) -> None: ...

class updateFolderPeers(TLObject):
    folder_peers: list[TLObject]
    pts: int
    pts_count: int
    def __init__(self, *, folder_peers: list[TLObject], pts: int, pts_count: int) -> None: ...

class updateGeoLiveViewed(TLObject):
    peer: TLObject
    msg_id: int
    def __init__(self, *, peer: TLObject, msg_id: int) -> None: ...

class updateGroupCall(TLObject):
    live_story: bool
    peer: TLObject | None
    call: TLObject
    def __init__(self, *, live_story: bool = ..., peer: TLObject | None = ..., call: TLObject) -> None: ...

class updateGroupCallChainBlocks(TLObject):
    call: TLObject
    sub_chain_id: int
    blocks: list[bytes]
    next_offset: int
    def __init__(self, *, call: TLObject, sub_chain_id: int, blocks: list[bytes], next_offset: int) -> None: ...

class updateGroupCallConnection(TLObject):
    presentation: bool
    params: TLObject
    def __init__(self, *, presentation: bool = ..., params: TLObject) -> None: ...

class updateGroupCallEncryptedMessage(TLObject):
    call: TLObject
    from_id: TLObject
    encrypted_message: bytes
    def __init__(self, *, call: TLObject, from_id: TLObject, encrypted_message: bytes) -> None: ...

class updateGroupCallMessage(TLObject):
    call: TLObject
    message: TLObject
    def __init__(self, *, call: TLObject, message: TLObject) -> None: ...

class updateGroupCallParticipants(TLObject):
    call: TLObject
    participants: list[TLObject]
    version: int
    def __init__(self, *, call: TLObject, participants: list[TLObject], version: int) -> None: ...

class updateInlineBotCallbackQuery(TLObject):
    query_id: int
    user_id: int
    msg_id: TLObject
    chat_instance: int
    data: bytes | None
    game_short_name: str | None
    def __init__(self, *, query_id: int, user_id: int, msg_id: TLObject, chat_instance: int, data: bytes | None = ..., game_short_name: str | None = ...) -> None: ...

class updateInlineBotWidgetQuery(TLObject):
    query_id: int
    query_type: TLObject
    user_id: int
    inline_message_id: TLObject
    chat_instance: int
    chat_type: str
    data: bytes
    widget_id: int | None
    wallet_card: TLObject | None
    def __init__(self, *, query_id: int, query_type: TLObject, user_id: int, inline_message_id: TLObject, chat_instance: int, chat_type: str, data: bytes, widget_id: int | None = ..., wallet_card: TLObject | None = ...) -> None: ...

class updateJoinChatWebViewDecision(TLObject):
    peer: TLObject
    query_id: int
    result: TLObject
    def __init__(self, *, peer: TLObject, query_id: int, result: TLObject) -> None: ...

class updateLangPack(TLObject):
    difference: TLObject
    def __init__(self, *, difference: TLObject) -> None: ...

class updateLangPackTooLong(TLObject):
    lang_code: str
    def __init__(self, *, lang_code: str) -> None: ...

class updateLoginToken(TLObject):
    def __init__(self) -> None: ...

class updateManagedBot(TLObject):
    user_id: int
    bot_id: int
    qts: int
    def __init__(self, *, user_id: int, bot_id: int, qts: int) -> None: ...

class updateMessageExtendedMedia(TLObject):
    peer: TLObject
    msg_id: int
    extended_media: list[TLObject]
    def __init__(self, *, peer: TLObject, msg_id: int, extended_media: list[TLObject]) -> None: ...

class updateMessageID(TLObject):
    id: int
    random_id: int
    def __init__(self, *, id: int, random_id: int) -> None: ...

class updateMessagePoll(TLObject):
    peer: TLObject | None
    msg_id: int | None
    top_msg_id: int | None
    poll_id: int
    poll: TLObject | None
    results: TLObject
    def __init__(self, *, peer: TLObject | None = ..., msg_id: int | None = ..., top_msg_id: int | None = ..., poll_id: int, poll: TLObject | None = ..., results: TLObject) -> None: ...

class updateMessagePollVote(TLObject):
    poll_id: int
    peer: TLObject
    options: list[bytes]
    positions: list[int]
    qts: int
    def __init__(self, *, poll_id: int, peer: TLObject, options: list[bytes], positions: list[int], qts: int) -> None: ...

class updateMessageReactions(TLObject):
    peer: TLObject
    msg_id: int
    top_msg_id: int | None
    saved_peer_id: TLObject | None
    reactions: TLObject
    def __init__(self, *, peer: TLObject, msg_id: int, top_msg_id: int | None = ..., saved_peer_id: TLObject | None = ..., reactions: TLObject) -> None: ...

class updateMessageWidgetData(TLObject):
    peer: TLObject
    msg_id: int
    public_data: str | None
    public_data_hash: int | None
    chat_data: str | None
    pts: int
    pts_count: int
    def __init__(self, *, peer: TLObject, msg_id: int, public_data: str | None = ..., public_data_hash: int | None = ..., chat_data: str | None = ..., pts: int, pts_count: int) -> None: ...

class updateMonoForumNoPaidException(TLObject):
    exception: bool
    channel_id: int
    saved_peer_id: TLObject
    def __init__(self, *, exception: bool = ..., channel_id: int, saved_peer_id: TLObject) -> None: ...

class updateMoveStickerSetToTop(TLObject):
    masks: bool
    emojis: bool
    stickerset: int
    def __init__(self, *, masks: bool = ..., emojis: bool = ..., stickerset: int) -> None: ...

class updateNewAuthorization(TLObject):
    unconfirmed: bool
    hash: int
    date: int | None
    device: str | None
    location: str | None
    def __init__(self, *, unconfirmed: bool = ..., hash: int, date: int | None = ..., device: str | None = ..., location: str | None = ...) -> None: ...

class updateNewBotConnection(TLObject):
    confirmed: bool
    bot_id: int
    date: int | None
    device: str | None
    location: str | None
    def __init__(self, *, confirmed: bool = ..., bot_id: int, date: int | None = ..., device: str | None = ..., location: str | None = ...) -> None: ...

class updateNewChannelMessage(TLObject):
    message: TLObject
    pts: int
    pts_count: int
    def __init__(self, *, message: TLObject, pts: int, pts_count: int) -> None: ...

class updateNewEncryptedMessage(TLObject):
    message: TLObject
    qts: int
    def __init__(self, *, message: TLObject, qts: int) -> None: ...

class updateNewEphemeralMessage(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class updateNewMessage(TLObject):
    message: TLObject
    pts: int
    pts_count: int
    def __init__(self, *, message: TLObject, pts: int, pts_count: int) -> None: ...

class updateNewQuickReply(TLObject):
    quick_reply: TLObject
    def __init__(self, *, quick_reply: TLObject) -> None: ...

class updateNewScheduledMessage(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class updateNewStickerSet(TLObject):
    stickerset: TLObject
    def __init__(self, *, stickerset: TLObject) -> None: ...

class updateNewStoryReaction(TLObject):
    story_id: int
    peer: TLObject
    reaction: TLObject
    def __init__(self, *, story_id: int, peer: TLObject, reaction: TLObject) -> None: ...

class updateNotifySettings(TLObject):
    peer: TLObject
    notify_settings: TLObject
    def __init__(self, *, peer: TLObject, notify_settings: TLObject) -> None: ...

class updatePaidReactionPrivacy(TLObject):
    private: TLObject
    def __init__(self, *, private: TLObject) -> None: ...

class updatePeerBlocked(TLObject):
    blocked: bool
    blocked_my_stories_from: bool
    peer_id: TLObject
    def __init__(self, *, blocked: bool = ..., blocked_my_stories_from: bool = ..., peer_id: TLObject) -> None: ...

class updatePeerHistoryTTL(TLObject):
    peer: TLObject
    ttl_period: int | None
    def __init__(self, *, peer: TLObject, ttl_period: int | None = ...) -> None: ...

class updatePeerLocated(TLObject):
    peers: list[TLObject]
    def __init__(self, *, peers: list[TLObject]) -> None: ...

class updatePeerSettings(TLObject):
    peer: TLObject
    settings: TLObject
    def __init__(self, *, peer: TLObject, settings: TLObject) -> None: ...

class updatePeerWallpaper(TLObject):
    wallpaper_overridden: bool
    peer: TLObject
    wallpaper: TLObject | None
    def __init__(self, *, wallpaper_overridden: bool = ..., peer: TLObject, wallpaper: TLObject | None = ...) -> None: ...

class updatePendingJoinRequests(TLObject):
    peer: TLObject
    requests_pending: int
    recent_requesters: list[int]
    def __init__(self, *, peer: TLObject, requests_pending: int, recent_requesters: list[int]) -> None: ...

class updatePhoneCall(TLObject):
    phone_call: TLObject
    def __init__(self, *, phone_call: TLObject) -> None: ...

class updatePhoneCallSignalingData(TLObject):
    phone_call_id: int
    data: bytes
    def __init__(self, *, phone_call_id: int, data: bytes) -> None: ...

class updatePinnedChannelMessages(TLObject):
    pinned: bool
    channel_id: int
    messages: list[int]
    pts: int
    pts_count: int
    def __init__(self, *, pinned: bool = ..., channel_id: int, messages: list[int], pts: int, pts_count: int) -> None: ...

class updatePinnedDialogs(TLObject):
    folder_id: int | None
    order: list[TLObject] | None
    def __init__(self, *, folder_id: int | None = ..., order: list[TLObject] | None = ...) -> None: ...

class updatePinnedForumTopic(TLObject):
    pinned: bool
    peer: TLObject
    topic_id: int
    def __init__(self, *, pinned: bool = ..., peer: TLObject, topic_id: int) -> None: ...

class updatePinnedForumTopics(TLObject):
    peer: TLObject
    order: list[int] | None
    def __init__(self, *, peer: TLObject, order: list[int] | None = ...) -> None: ...

class updatePinnedMessages(TLObject):
    pinned: bool
    peer: TLObject
    messages: list[int]
    pts: int
    pts_count: int
    def __init__(self, *, pinned: bool = ..., peer: TLObject, messages: list[int], pts: int, pts_count: int) -> None: ...

class updatePinnedSavedDialogs(TLObject):
    order: list[TLObject] | None
    def __init__(self, *, order: list[TLObject] | None = ...) -> None: ...

class updatePrivacy(TLObject):
    key: TLObject
    rules: list[TLObject]
    def __init__(self, *, key: TLObject, rules: list[TLObject]) -> None: ...

class updatePtsChanged(TLObject):
    def __init__(self) -> None: ...

class updateQuickReplies(TLObject):
    quick_replies: list[TLObject]
    def __init__(self, *, quick_replies: list[TLObject]) -> None: ...

class updateQuickReplyMessage(TLObject):
    message: TLObject
    def __init__(self, *, message: TLObject) -> None: ...

class updateReadChannelDiscussionInbox(TLObject):
    channel_id: int
    top_msg_id: int
    read_max_id: int
    broadcast_id: int | None
    broadcast_post: int | None
    def __init__(self, *, channel_id: int, top_msg_id: int, read_max_id: int, broadcast_id: int | None = ..., broadcast_post: int | None = ...) -> None: ...

class updateReadChannelDiscussionOutbox(TLObject):
    channel_id: int
    top_msg_id: int
    read_max_id: int
    def __init__(self, *, channel_id: int, top_msg_id: int, read_max_id: int) -> None: ...

class updateReadChannelInbox(TLObject):
    folder_id: int | None
    channel_id: int
    max_id: int
    still_unread_count: int
    pts: int
    def __init__(self, *, folder_id: int | None = ..., channel_id: int, max_id: int, still_unread_count: int, pts: int) -> None: ...

class updateReadChannelOutbox(TLObject):
    channel_id: int
    max_id: int
    def __init__(self, *, channel_id: int, max_id: int) -> None: ...

class updateReadFeaturedEmojiStickers(TLObject):
    def __init__(self) -> None: ...

class updateReadFeaturedStickers(TLObject):
    def __init__(self) -> None: ...

class updateReadHistoryInbox(TLObject):
    folder_id: int | None
    peer: TLObject
    top_msg_id: int | None
    max_id: int
    still_unread_count: int
    pts: int
    pts_count: int
    def __init__(self, *, folder_id: int | None = ..., peer: TLObject, top_msg_id: int | None = ..., max_id: int, still_unread_count: int, pts: int, pts_count: int) -> None: ...

class updateReadHistoryOutbox(TLObject):
    peer: TLObject
    max_id: int
    pts: int
    pts_count: int
    def __init__(self, *, peer: TLObject, max_id: int, pts: int, pts_count: int) -> None: ...

class updateReadMessagesContents(TLObject):
    messages: list[int]
    pts: int
    pts_count: int
    date: int | None
    def __init__(self, *, messages: list[int], pts: int, pts_count: int, date: int | None = ...) -> None: ...

class updateReadMonoForumInbox(TLObject):
    channel_id: int
    saved_peer_id: TLObject
    read_max_id: int
    def __init__(self, *, channel_id: int, saved_peer_id: TLObject, read_max_id: int) -> None: ...

class updateReadMonoForumOutbox(TLObject):
    channel_id: int
    saved_peer_id: TLObject
    read_max_id: int
    def __init__(self, *, channel_id: int, saved_peer_id: TLObject, read_max_id: int) -> None: ...

class updateReadStories(TLObject):
    peer: TLObject
    max_id: int
    def __init__(self, *, peer: TLObject, max_id: int) -> None: ...

class updateRecentEmojiStatuses(TLObject):
    def __init__(self) -> None: ...

class updateRecentReactions(TLObject):
    def __init__(self) -> None: ...

class updateRecentStickers(TLObject):
    def __init__(self) -> None: ...

class updateSavedDialogPinned(TLObject):
    pinned: bool
    peer: TLObject
    def __init__(self, *, pinned: bool = ..., peer: TLObject) -> None: ...

class updateSavedGifs(TLObject):
    def __init__(self) -> None: ...

class updateSavedReactionTags(TLObject):
    def __init__(self) -> None: ...

class updateSavedRingtones(TLObject):
    def __init__(self) -> None: ...

class updateSentPhoneCode(TLObject):
    sent_code: TLObject
    def __init__(self, *, sent_code: TLObject) -> None: ...

class updateSentStoryReaction(TLObject):
    peer: TLObject
    story_id: int
    reaction: TLObject
    def __init__(self, *, peer: TLObject, story_id: int, reaction: TLObject) -> None: ...

class updateSentWalletTransaction(TLObject):
    gasless: bool
    msg_hash: str
    transaction: TLObject | None
    def __init__(self, *, gasless: bool = ..., msg_hash: str, transaction: TLObject | None = ...) -> None: ...

class updateServiceNotification(TLObject):
    popup: bool
    invert_media: bool
    inbox_date: int | None
    type: str
    message: str
    media: TLObject
    entities: list[TLObject]
    def __init__(self, *, popup: bool = ..., invert_media: bool = ..., inbox_date: int | None = ..., type: str, message: str, media: TLObject, entities: list[TLObject]) -> None: ...

class updateShort(TLObject):
    update: TLObject
    date: int
    def __init__(self, *, update: TLObject, date: int) -> None: ...

class updateShortChatMessage(TLObject):
    out: bool
    mentioned: bool
    media_unread: bool
    silent: bool
    id: int
    from_id: int
    chat_id: int
    message: str
    pts: int
    pts_count: int
    date: int
    fwd_from: TLObject | None
    via_bot_id: int | None
    reply_to: TLObject | None
    entities: list[TLObject] | None
    ttl_period: int | None
    def __init__(self, *, out: bool = ..., mentioned: bool = ..., media_unread: bool = ..., silent: bool = ..., id: int, from_id: int, chat_id: int, message: str, pts: int, pts_count: int, date: int, fwd_from: TLObject | None = ..., via_bot_id: int | None = ..., reply_to: TLObject | None = ..., entities: list[TLObject] | None = ..., ttl_period: int | None = ...) -> None: ...

class updateShortMessage(TLObject):
    out: bool
    mentioned: bool
    media_unread: bool
    silent: bool
    id: int
    user_id: int
    message: str
    pts: int
    pts_count: int
    date: int
    fwd_from: TLObject | None
    via_bot_id: int | None
    reply_to: TLObject | None
    entities: list[TLObject] | None
    ttl_period: int | None
    def __init__(self, *, out: bool = ..., mentioned: bool = ..., media_unread: bool = ..., silent: bool = ..., id: int, user_id: int, message: str, pts: int, pts_count: int, date: int, fwd_from: TLObject | None = ..., via_bot_id: int | None = ..., reply_to: TLObject | None = ..., entities: list[TLObject] | None = ..., ttl_period: int | None = ...) -> None: ...

class updateShortSentMessage(TLObject):
    out: bool
    id: int
    pts: int
    pts_count: int
    date: int
    media: TLObject | None
    entities: list[TLObject] | None
    ttl_period: int | None
    def __init__(self, *, out: bool = ..., id: int, pts: int, pts_count: int, date: int, media: TLObject | None = ..., entities: list[TLObject] | None = ..., ttl_period: int | None = ...) -> None: ...

class updateSmsJob(TLObject):
    job_id: str
    def __init__(self, *, job_id: str) -> None: ...

class updateStarGiftAuctionState(TLObject):
    gift_id: int
    state: TLObject
    def __init__(self, *, gift_id: int, state: TLObject) -> None: ...

class updateStarGiftAuctionUserState(TLObject):
    gift_id: int
    user_state: TLObject
    def __init__(self, *, gift_id: int, user_state: TLObject) -> None: ...

class updateStarGiftCraftFail(TLObject):
    def __init__(self) -> None: ...

class updateStarsBalance(TLObject):
    balance: TLObject
    def __init__(self, *, balance: TLObject) -> None: ...

class updateStarsRevenueStatus(TLObject):
    peer: TLObject
    status: TLObject
    def __init__(self, *, peer: TLObject, status: TLObject) -> None: ...

class updateStickerSets(TLObject):
    masks: bool
    emojis: bool
    def __init__(self, *, masks: bool = ..., emojis: bool = ...) -> None: ...

class updateStickerSetsOrder(TLObject):
    masks: bool
    emojis: bool
    order: list[int]
    def __init__(self, *, masks: bool = ..., emojis: bool = ..., order: list[int]) -> None: ...

class updateStoriesStealthMode(TLObject):
    stealth_mode: TLObject
    def __init__(self, *, stealth_mode: TLObject) -> None: ...

class updateStory(TLObject):
    peer: TLObject
    story: TLObject
    def __init__(self, *, peer: TLObject, story: TLObject) -> None: ...

class updateStoryID(TLObject):
    id: int
    random_id: int
    def __init__(self, *, id: int, random_id: int) -> None: ...

class updateTheme(TLObject):
    theme: TLObject
    def __init__(self, *, theme: TLObject) -> None: ...

class updateTranscribedAudio(TLObject):
    pending: bool
    peer: TLObject
    msg_id: int
    transcription_id: int
    text: str
    def __init__(self, *, pending: bool = ..., peer: TLObject, msg_id: int, transcription_id: int, text: str) -> None: ...

class updateTranscribedAudioFile(TLObject):
    pending: bool
    transcription_id: int
    text: str
    def __init__(self, *, pending: bool = ..., transcription_id: int, text: str) -> None: ...

class updateUser(TLObject):
    user_id: int
    def __init__(self, *, user_id: int) -> None: ...

class updateUserEmojiStatus(TLObject):
    user_id: int
    emoji_status: TLObject
    def __init__(self, *, user_id: int, emoji_status: TLObject) -> None: ...

class updateUserName(TLObject):
    user_id: int
    first_name: str
    last_name: str
    usernames: list[TLObject]
    def __init__(self, *, user_id: int, first_name: str, last_name: str, usernames: list[TLObject]) -> None: ...

class updateUserPhone(TLObject):
    user_id: int
    phone: str
    def __init__(self, *, user_id: int, phone: str) -> None: ...

class updateUserStatus(TLObject):
    user_id: int
    status: TLObject
    def __init__(self, *, user_id: int, status: TLObject) -> None: ...

class updateUserTyping(TLObject):
    user_id: int
    top_msg_id: int | None
    action: TLObject
    def __init__(self, *, user_id: int, top_msg_id: int | None = ..., action: TLObject) -> None: ...

class updateWalletGaslessInfo(TLObject):
    available: bool
    left: int
    reset_at: int
    min_amount: int
    relayer_address: str
    def __init__(self, *, available: bool = ..., left: int, reset_at: int, min_amount: int, relayer_address: str) -> None: ...

class updateWalletState(TLObject):
    state: TLObject
    def __init__(self, *, state: TLObject) -> None: ...

class updateWalletTonConnectPendingDisconnect(TLObject):
    session_ids: list[int]
    def __init__(self, *, session_ids: list[int]) -> None: ...

class updateWalletTonConnectSession(TLObject):
    session: TLObject
    def __init__(self, *, session: TLObject) -> None: ...

class updateWebBrowserException(TLObject):
    delete: bool
    open_external_browser: bool
    exception: TLObject
    def __init__(self, *, delete: bool = ..., open_external_browser: bool = ..., exception: TLObject) -> None: ...

class updateWebBrowserSettings(TLObject):
    open_external_browser: bool
    display_close_button: bool
    def __init__(self, *, open_external_browser: bool = ..., display_close_button: bool = ...) -> None: ...

class updateWebPage(TLObject):
    webpage: TLObject
    pts: int
    pts_count: int
    def __init__(self, *, webpage: TLObject, pts: int, pts_count: int) -> None: ...

class updateWebViewResultSent(TLObject):
    query_id: int
    def __init__(self, *, query_id: int) -> None: ...

class updates(TLObject):
    updates: list[TLObject]
    users: list[TLObject]
    chats: list[TLObject]
    date: int
    seq: int
    def __init__(self, *, updates: list[TLObject], users: list[TLObject], chats: list[TLObject], date: int, seq: int) -> None: ...
    class channelDifference(TLObject):
        final: bool
        pts: int
        timeout: int | None
        new_messages: list[TLObject]
        other_updates: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, final: bool = ..., pts: int, timeout: int | None = ..., new_messages: list[TLObject], other_updates: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class channelDifferenceEmpty(TLObject):
        final: bool
        pts: int
        timeout: int | None
        def __init__(self, *, final: bool = ..., pts: int, timeout: int | None = ...) -> None: ...

    class channelDifferenceTooLong(TLObject):
        final: bool
        timeout: int | None
        dialog: TLObject
        messages: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, final: bool = ..., timeout: int | None = ..., dialog: TLObject, messages: list[TLObject], chats: list[TLObject], users: list[TLObject]) -> None: ...

    class difference(TLObject):
        new_messages: list[TLObject]
        new_encrypted_messages: list[TLObject]
        other_updates: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        state: TLObject
        def __init__(self, *, new_messages: list[TLObject], new_encrypted_messages: list[TLObject], other_updates: list[TLObject], chats: list[TLObject], users: list[TLObject], state: TLObject) -> None: ...

    class differenceEmpty(TLObject):
        date: int
        seq: int
        def __init__(self, *, date: int, seq: int) -> None: ...

    class differenceSlice(TLObject):
        new_messages: list[TLObject]
        new_encrypted_messages: list[TLObject]
        other_updates: list[TLObject]
        chats: list[TLObject]
        users: list[TLObject]
        intermediate_state: TLObject
        def __init__(self, *, new_messages: list[TLObject], new_encrypted_messages: list[TLObject], other_updates: list[TLObject], chats: list[TLObject], users: list[TLObject], intermediate_state: TLObject) -> None: ...

    class differenceTooLong(TLObject):
        pts: int
        def __init__(self, *, pts: int) -> None: ...

    class getChannelDifference(TLObject):
        force: bool
        channel: TLObject
        filter: TLObject
        pts: int
        limit: int
        def __init__(self, *, force: bool = ..., channel: TLObject, filter: TLObject, pts: int, limit: int) -> None: ...

    class getDifference(TLObject):
        pts: int
        pts_limit: int | None
        pts_total_limit: int | None
        date: int
        qts: int
        qts_limit: int | None
        def __init__(self, *, pts: int, pts_limit: int | None = ..., pts_total_limit: int | None = ..., date: int, qts: int, qts_limit: int | None = ...) -> None: ...

    class getState(TLObject):
        def __init__(self) -> None: ...

    class state(TLObject):
        pts: int
        qts: int
        date: int
        seq: int
        unread_count: int
        def __init__(self, *, pts: int, qts: int, date: int, seq: int, unread_count: int) -> None: ...


class updatesCombined(TLObject):
    updates: list[TLObject]
    users: list[TLObject]
    chats: list[TLObject]
    date: int
    seq_start: int
    seq: int
    def __init__(self, *, updates: list[TLObject], users: list[TLObject], chats: list[TLObject], date: int, seq_start: int, seq: int) -> None: ...

class updatesTooLong(TLObject):
    def __init__(self) -> None: ...

class upload:
    class cdnFile(TLObject):
        bytes: bytes
        def __init__(self, *, bytes: bytes) -> None: ...

    class cdnFileReuploadNeeded(TLObject):
        request_token: bytes
        def __init__(self, *, request_token: bytes) -> None: ...

    class file(TLObject):
        type: TLObject
        mtime: int
        bytes: bytes
        def __init__(self, *, type: TLObject, mtime: int, bytes: bytes) -> None: ...

    class fileCdnRedirect(TLObject):
        dc_id: int
        file_token: bytes
        encryption_key: bytes
        encryption_iv: bytes
        file_hashes: list[TLObject]
        def __init__(self, *, dc_id: int, file_token: bytes, encryption_key: bytes, encryption_iv: bytes, file_hashes: list[TLObject]) -> None: ...

    class getCdnFile(TLObject):
        file_token: bytes
        offset: int
        limit: int
        def __init__(self, *, file_token: bytes, offset: int, limit: int) -> None: ...

    class getCdnFileHashes(TLObject):
        file_token: bytes
        offset: int
        def __init__(self, *, file_token: bytes, offset: int) -> None: ...

    class getFile(TLObject):
        precise: bool
        cdn_supported: bool
        location: TLObject
        offset: int
        limit: int
        def __init__(self, *, precise: bool = ..., cdn_supported: bool = ..., location: TLObject, offset: int, limit: int) -> None: ...

    class getFileHashes(TLObject):
        location: TLObject
        offset: int
        def __init__(self, *, location: TLObject, offset: int) -> None: ...

    class getWebFile(TLObject):
        location: TLObject
        offset: int
        limit: int
        def __init__(self, *, location: TLObject, offset: int, limit: int) -> None: ...

    class reuploadCdnFile(TLObject):
        file_token: bytes
        request_token: bytes
        def __init__(self, *, file_token: bytes, request_token: bytes) -> None: ...

    class saveBigFilePart(TLObject):
        file_id: int
        file_part: int
        file_total_parts: int
        bytes: bytes
        def __init__(self, *, file_id: int, file_part: int, file_total_parts: int, bytes: bytes) -> None: ...

    class saveFilePart(TLObject):
        file_id: int
        file_part: int
        bytes: bytes
        def __init__(self, *, file_id: int, file_part: int, bytes: bytes) -> None: ...

    class webFile(TLObject):
        size: int
        mime_type: str
        file_type: TLObject
        mtime: int
        bytes: bytes
        def __init__(self, *, size: int, mime_type: str, file_type: TLObject, mtime: int, bytes: bytes) -> None: ...

class urlAuthResultAccepted(TLObject):
    url: str | None
    def __init__(self, *, url: str | None = ...) -> None: ...

class urlAuthResultDefault(TLObject):
    def __init__(self) -> None: ...

class urlAuthResultRequest(TLObject):
    request_write_access: bool
    request_phone_number: bool
    match_codes_first: bool
    is_app: bool
    request_wallet: bool
    bot: TLObject
    domain: str
    browser: str | None
    platform: str | None
    ip: str | None
    region: str | None
    match_codes: list[str] | None
    user_id_hint: int | None
    verified_app_name: str | None
    tc_session_id: int | None
    tc_client_id: str | None
    def __init__(self, *, request_write_access: bool = ..., request_phone_number: bool = ..., match_codes_first: bool = ..., is_app: bool = ..., request_wallet: bool = ..., bot: TLObject, domain: str, browser: str | None = ..., platform: str | None = ..., ip: str | None = ..., region: str | None = ..., match_codes: list[str] | None = ..., user_id_hint: int | None = ..., verified_app_name: str | None = ..., tc_session_id: int | None = ..., tc_client_id: str | None = ...) -> None: ...

class user(TLObject):
    self_: bool
    contact: bool
    mutual_contact: bool
    deleted: bool
    bot: bool
    bot_chat_history: bool
    bot_nochats: bool
    verified: bool
    restricted: bool
    min: bool
    bot_inline_geo: bool
    support: bool
    scam: bool
    apply_min_photo: bool
    fake: bool
    bot_attach_menu: bool
    premium: bool
    attach_menu_enabled: bool
    bot_can_edit: bool
    close_friend: bool
    stories_hidden: bool
    stories_unavailable: bool
    contact_require_premium: bool
    bot_business: bool
    bot_has_main_app: bool
    bot_forum_view: bool
    bot_forum_can_manage_topics: bool
    bot_can_manage_bots: bool
    bot_guestchat: bool
    bot_guard: bool
    bot_forum_sidebar: bool
    id: int
    access_hash: int | None
    first_name: str | None
    last_name: str | None
    username: str | None
    phone: str | None
    photo: TLObject | None
    status: TLObject | None
    bot_info_version: int | None
    restriction_reason: list[TLObject] | None
    bot_inline_placeholder: str | None
    lang_code: str | None
    emoji_status: TLObject | None
    usernames: list[TLObject] | None
    stories_max_id: TLObject | None
    color: TLObject | None
    profile_color: TLObject | None
    bot_active_users: int | None
    bot_verification_icon: int | None
    send_paid_messages_stars: int | None
    linked_community_id: int | None
    def __init__(self, *, self_: bool = ..., contact: bool = ..., mutual_contact: bool = ..., deleted: bool = ..., bot: bool = ..., bot_chat_history: bool = ..., bot_nochats: bool = ..., verified: bool = ..., restricted: bool = ..., min: bool = ..., bot_inline_geo: bool = ..., support: bool = ..., scam: bool = ..., apply_min_photo: bool = ..., fake: bool = ..., bot_attach_menu: bool = ..., premium: bool = ..., attach_menu_enabled: bool = ..., bot_can_edit: bool = ..., close_friend: bool = ..., stories_hidden: bool = ..., stories_unavailable: bool = ..., contact_require_premium: bool = ..., bot_business: bool = ..., bot_has_main_app: bool = ..., bot_forum_view: bool = ..., bot_forum_can_manage_topics: bool = ..., bot_can_manage_bots: bool = ..., bot_guestchat: bool = ..., bot_guard: bool = ..., bot_forum_sidebar: bool = ..., id: int, access_hash: int | None = ..., first_name: str | None = ..., last_name: str | None = ..., username: str | None = ..., phone: str | None = ..., photo: TLObject | None = ..., status: TLObject | None = ..., bot_info_version: int | None = ..., restriction_reason: list[TLObject] | None = ..., bot_inline_placeholder: str | None = ..., lang_code: str | None = ..., emoji_status: TLObject | None = ..., usernames: list[TLObject] | None = ..., stories_max_id: TLObject | None = ..., color: TLObject | None = ..., profile_color: TLObject | None = ..., bot_active_users: int | None = ..., bot_verification_icon: int | None = ..., send_paid_messages_stars: int | None = ..., linked_community_id: int | None = ...) -> None: ...

class userEmpty(TLObject):
    id: int
    def __init__(self, *, id: int) -> None: ...

class userFull(TLObject):
    blocked: bool
    phone_calls_available: bool
    phone_calls_private: bool
    can_pin_message: bool
    has_scheduled: bool
    video_calls_available: bool
    voice_messages_forbidden: bool
    translations_disabled: bool
    stories_pinned_available: bool
    blocked_my_stories_from: bool
    wallpaper_overridden: bool
    contact_require_premium: bool
    read_dates_private: bool
    sponsored_enabled: bool
    can_view_revenue: bool
    bot_can_manage_emoji_status: bool
    display_gifts_button: bool
    noforwards_my_enabled: bool
    noforwards_peer_enabled: bool
    unofficial_security_risk: bool
    id: int
    about: str | None
    settings: TLObject
    personal_photo: TLObject | None
    profile_photo: TLObject | None
    fallback_photo: TLObject | None
    notify_settings: TLObject
    bot_info: TLObject | None
    pinned_msg_id: int | None
    common_chats_count: int
    folder_id: int | None
    ttl_period: int | None
    theme: TLObject | None
    private_forward_name: str | None
    bot_group_admin_rights: TLObject | None
    bot_broadcast_admin_rights: TLObject | None
    wallpaper: TLObject | None
    stories: TLObject | None
    business_work_hours: TLObject | None
    business_location: TLObject | None
    business_greeting_message: TLObject | None
    business_away_message: TLObject | None
    business_intro: TLObject | None
    birthday: TLObject | None
    personal_channel_id: int | None
    personal_channel_message: int | None
    stargifts_count: int | None
    starref_program: TLObject | None
    bot_verification: TLObject | None
    send_paid_messages_stars: int | None
    disallowed_gifts: TLObject | None
    stars_rating: TLObject | None
    stars_my_pending_rating: TLObject | None
    stars_my_pending_rating_date: int | None
    main_tab: TLObject | None
    saved_music: TLObject | None
    note: TLObject | None
    bot_manager_id: int | None
    wallet_card: TLObject | None
    share_theme: TLObject | None
    def __init__(self, *, blocked: bool = ..., phone_calls_available: bool = ..., phone_calls_private: bool = ..., can_pin_message: bool = ..., has_scheduled: bool = ..., video_calls_available: bool = ..., voice_messages_forbidden: bool = ..., translations_disabled: bool = ..., stories_pinned_available: bool = ..., blocked_my_stories_from: bool = ..., wallpaper_overridden: bool = ..., contact_require_premium: bool = ..., read_dates_private: bool = ..., sponsored_enabled: bool = ..., can_view_revenue: bool = ..., bot_can_manage_emoji_status: bool = ..., display_gifts_button: bool = ..., noforwards_my_enabled: bool = ..., noforwards_peer_enabled: bool = ..., unofficial_security_risk: bool = ..., id: int, about: str | None = ..., settings: TLObject, personal_photo: TLObject | None = ..., profile_photo: TLObject | None = ..., fallback_photo: TLObject | None = ..., notify_settings: TLObject, bot_info: TLObject | None = ..., pinned_msg_id: int | None = ..., common_chats_count: int, folder_id: int | None = ..., ttl_period: int | None = ..., theme: TLObject | None = ..., private_forward_name: str | None = ..., bot_group_admin_rights: TLObject | None = ..., bot_broadcast_admin_rights: TLObject | None = ..., wallpaper: TLObject | None = ..., stories: TLObject | None = ..., business_work_hours: TLObject | None = ..., business_location: TLObject | None = ..., business_greeting_message: TLObject | None = ..., business_away_message: TLObject | None = ..., business_intro: TLObject | None = ..., birthday: TLObject | None = ..., personal_channel_id: int | None = ..., personal_channel_message: int | None = ..., stargifts_count: int | None = ..., starref_program: TLObject | None = ..., bot_verification: TLObject | None = ..., send_paid_messages_stars: int | None = ..., disallowed_gifts: TLObject | None = ..., stars_rating: TLObject | None = ..., stars_my_pending_rating: TLObject | None = ..., stars_my_pending_rating_date: int | None = ..., main_tab: TLObject | None = ..., saved_music: TLObject | None = ..., note: TLObject | None = ..., bot_manager_id: int | None = ..., wallet_card: TLObject | None = ..., share_theme: TLObject | None = ...) -> None: ...

class userProfilePhoto(TLObject):
    has_video: bool
    personal: bool
    photo_id: int
    stripped_thumb: bytes | None
    dc_id: int
    def __init__(self, *, has_video: bool = ..., personal: bool = ..., photo_id: int, stripped_thumb: bytes | None = ..., dc_id: int) -> None: ...

class userProfilePhotoEmpty(TLObject):
    def __init__(self) -> None: ...

class userStatusEmpty(TLObject):
    def __init__(self) -> None: ...

class userStatusLastMonth(TLObject):
    by_me: bool
    def __init__(self, *, by_me: bool = ...) -> None: ...

class userStatusLastWeek(TLObject):
    by_me: bool
    def __init__(self, *, by_me: bool = ...) -> None: ...

class userStatusOffline(TLObject):
    was_online: int
    def __init__(self, *, was_online: int) -> None: ...

class userStatusOnline(TLObject):
    expires: int
    def __init__(self, *, expires: int) -> None: ...

class userStatusRecently(TLObject):
    by_me: bool
    def __init__(self, *, by_me: bool = ...) -> None: ...

class userWallet(TLObject):
    address: str
    balance: int
    public_key: bytes | None
    state_init: bytes | None
    def __init__(self, *, address: str, balance: int, public_key: bytes | None = ..., state_init: bytes | None = ...) -> None: ...

class username(TLObject):
    editable: bool
    active: bool
    deletable: bool
    expired: bool
    username: str
    def __init__(self, *, editable: bool = ..., active: bool = ..., deletable: bool = ..., expired: bool = ..., username: str) -> None: ...

class users:
    class getFullUser(TLObject):
        id: TLObject
        def __init__(self, *, id: TLObject) -> None: ...

    class getRequirementsToContact(TLObject):
        id: list[TLObject]
        def __init__(self, *, id: list[TLObject]) -> None: ...

    class getSavedMusic(TLObject):
        id: TLObject
        offset: int
        limit: int
        hash: int
        def __init__(self, *, id: TLObject, offset: int, limit: int, hash: int) -> None: ...

    class getSavedMusicByID(TLObject):
        id: TLObject
        documents: list[TLObject]
        def __init__(self, *, id: TLObject, documents: list[TLObject]) -> None: ...

    class getUsers(TLObject):
        id: list[TLObject]
        def __init__(self, *, id: list[TLObject]) -> None: ...

    class savedMusic(TLObject):
        count: int
        documents: list[TLObject]
        def __init__(self, *, count: int, documents: list[TLObject]) -> None: ...

    class savedMusicNotModified(TLObject):
        count: int
        def __init__(self, *, count: int) -> None: ...

    class setSecureValueErrors(TLObject):
        id: TLObject
        errors: list[TLObject]
        def __init__(self, *, id: TLObject, errors: list[TLObject]) -> None: ...

    class suggestBirthday(TLObject):
        id: TLObject
        birthday: TLObject
        def __init__(self, *, id: TLObject, birthday: TLObject) -> None: ...

    class userFull(TLObject):
        full_user: TLObject
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, full_user: TLObject, chats: list[TLObject], users: list[TLObject]) -> None: ...

    class users(TLObject):
        users: list[TLObject]
        def __init__(self, *, users: list[TLObject]) -> None: ...

    class usersSlice(TLObject):
        count: int
        users: list[TLObject]
        def __init__(self, *, count: int, users: list[TLObject]) -> None: ...

class videoSize(TLObject):
    type: str
    w: int
    h: int
    size: int
    video_start_ts: float | None
    def __init__(self, *, type: str, w: int, h: int, size: int, video_start_ts: float | None = ...) -> None: ...

class videoSizeEmojiMarkup(TLObject):
    emoji_id: int
    background_colors: list[int]
    def __init__(self, *, emoji_id: int, background_colors: list[int]) -> None: ...

class videoSizeStickerMarkup(TLObject):
    stickerset: TLObject
    sticker_id: int
    background_colors: list[int]
    def __init__(self, *, stickerset: TLObject, sticker_id: int, background_colors: list[int]) -> None: ...

class wallPaper(TLObject):
    id: int
    creator: bool
    default: bool
    pattern: bool
    dark: bool
    access_hash: int
    slug: str
    document: TLObject
    settings: TLObject | None
    def __init__(self, *, id: int, creator: bool = ..., default: bool = ..., pattern: bool = ..., dark: bool = ..., access_hash: int, slug: str, document: TLObject, settings: TLObject | None = ...) -> None: ...

class wallPaperNoFile(TLObject):
    id: int
    default: bool
    dark: bool
    settings: TLObject | None
    def __init__(self, *, id: int, default: bool = ..., dark: bool = ..., settings: TLObject | None = ...) -> None: ...

class wallPaperSettings(TLObject):
    blur: bool
    motion: bool
    background_color: int | None
    second_background_color: int | None
    third_background_color: int | None
    fourth_background_color: int | None
    intensity: int | None
    rotation: int | None
    emoticon: str | None
    def __init__(self, *, blur: bool = ..., motion: bool = ..., background_color: int | None = ..., second_background_color: int | None = ..., third_background_color: int | None = ..., fourth_background_color: int | None = ..., intensity: int | None = ..., rotation: int | None = ..., emoticon: str | None = ...) -> None: ...

class wallet:
    class card(TLObject):
        stickers: list[TLObject] | None
        bg_nft_item: TLObject | None
        address: str
        balance: int
        def __init__(self, *, stickers: list[TLObject] | None = ..., bg_nft_item: TLObject | None = ..., address: str, balance: int) -> None: ...

    class cardSticker(TLObject):
        coordinates: TLObject
        nft: TLObject
        def __init__(self, *, coordinates: TLObject, nft: TLObject) -> None: ...

    class disableBackup(TLObject):
        password: TLObject | None
        new_public_key: bytes | None
        proof: TLObject | None
        def __init__(self, *, password: TLObject | None = ..., new_public_key: bytes | None = ..., proof: TLObject | None = ...) -> None: ...

    class enableBackup(TLObject):
        parts: list[bytes]
        new_public_key: bytes | None
        proof: TLObject | None
        def __init__(self, *, parts: list[bytes], new_public_key: bytes | None = ..., proof: TLObject | None = ...) -> None: ...

    class encryptedSecretPhrasePart(TLObject):
        data: bytes
        def __init__(self, *, data: bytes) -> None: ...

    class existingBalance(TLObject):
        has_balance: bool
        url: str
        def __init__(self, *, has_balance: bool = ..., url: str) -> None: ...

    class exportSecretPhrase(TLObject):
        password: TLObject | None
        def __init__(self, *, password: TLObject | None = ...) -> None: ...

    class fetchEncryptedSecretPhrasePart(TLObject):
        token: str
        public_key: bytes
        def __init__(self, *, token: str, public_key: bytes) -> None: ...

    class getBackupHolderDcs(TLObject):
        def __init__(self) -> None: ...

    class getExistingWaltBalance(TLObject):
        def __init__(self) -> None: ...

    class getGaslessInfo(TLObject):
        def __init__(self) -> None: ...

    class getNfts(TLObject):
        offset: str
        limit: int
        def __init__(self, *, offset: str, limit: int) -> None: ...

    class getProofChallenge(TLObject):
        def __init__(self) -> None: ...

    class getState(TLObject):
        def __init__(self) -> None: ...

    class getTransactions(TLObject):
        inbound: bool
        outbound: bool
        offset: str
        limit: int
        def __init__(self, *, inbound: bool = ..., outbound: bool = ..., offset: str, limit: int) -> None: ...

    class getTransactionsByIDs(TLObject):
        id: list[str]
        def __init__(self, *, id: list[str]) -> None: ...

    class getTransactionsByMsgHash(TLObject):
        msg_hash: list[str]
        def __init__(self, *, msg_hash: list[str]) -> None: ...

    class getUserAddresses(TLObject):
        force: bool
        id: list[TLObject]
        addresses: list[str]
        def __init__(self, *, force: bool = ..., id: list[TLObject], addresses: list[str]) -> None: ...

    class holderDc(TLObject):
        dc: int
        public_key: bytes
        def __init__(self, *, dc: int, public_key: bytes) -> None: ...

    class nftAttribute(TLObject):
        trait_type: str
        value: str
        def __init__(self, *, trait_type: str, value: str) -> None: ...

    class nftItem(TLObject):
        collection_address: str | None
        address: str
        owner_address: str
        index: str
        name: str | None
        description: str | None
        image: TLObject | None
        image_small: TLObject | None
        content_url: TLObject | None
        lottie: TLObject | None
        attributes: list[TLObject] | None
        extra: TLObject | None
        gift: TLObject | None
        def __init__(self, *, collection_address: str | None = ..., address: str, owner_address: str, index: str, name: str | None = ..., description: str | None = ..., image: TLObject | None = ..., image_small: TLObject | None = ..., content_url: TLObject | None = ..., lottie: TLObject | None = ..., attributes: list[TLObject] | None = ..., extra: TLObject | None = ..., gift: TLObject | None = ...) -> None: ...

    class nftItems(TLObject):
        items: list[TLObject]
        next_offset: str | None
        def __init__(self, *, items: list[TLObject], next_offset: str | None = ...) -> None: ...

    class proofChallenge(TLObject):
        payload: str
        expires: int
        domain: str
        def __init__(self, *, payload: str, expires: int, domain: str) -> None: ...

    class replaceWallet(TLObject):
        wallet: TLObject
        password: TLObject | None
        def __init__(self, *, wallet: TLObject, password: TLObject | None = ...) -> None: ...

    class secretPhraseParts(TLObject):
        token: str
        dcs: list[int]
        def __init__(self, *, token: str, dcs: list[int]) -> None: ...

    class sendTransfer(TLObject):
        data_normal: bytes
        data_gasless: bytes | None
        user_id: TLObject
        random_id: int
        def __init__(self, *, data_normal: bytes, data_gasless: bytes | None = ..., user_id: TLObject, random_id: int) -> None: ...

    class setCardStickers(TLObject):
        stickers: list[TLObject]
        bg_nft_address: str | None
        def __init__(self, *, stickers: list[TLObject], bg_nft_address: str | None = ...) -> None: ...

    class tonConnectChallenge(TLObject):
        challenge: bytes
        event_id: int
        def __init__(self, *, challenge: bytes, event_id: int) -> None: ...

    class tonConnectClaimRequest(TLObject):
        declined: bool
        session_id: int
        msg_id: int
        app_request_id: str
        challenge_answer: bytes | None
        def __init__(self, *, declined: bool = ..., session_id: int, msg_id: int, app_request_id: str, challenge_answer: bytes | None = ...) -> None: ...

    class tonConnectCloseSession(TLObject):
        session_id: int
        body: bytes | None
        def __init__(self, *, session_id: int, body: bytes | None = ...) -> None: ...

    class tonConnectCreateSession(TLObject):
        dapp_client_id: str
        manifest_url: str
        def __init__(self, *, dapp_client_id: str, manifest_url: str) -> None: ...

    class tonConnectGetPending(TLObject):
        dapp_client_id: str | None
        session_id: int | None
        def __init__(self, *, dapp_client_id: str | None = ..., session_id: int | None = ...) -> None: ...

    class tonConnectGetSessions(TLObject):
        def __init__(self) -> None: ...

    class tonConnectNextEventId(TLObject):
        session_id: int
        def __init__(self, *, session_id: int) -> None: ...

    class tonConnectPending(TLObject):
        session: TLObject
        requests: list[TLObject]
        def __init__(self, *, session: TLObject, requests: list[TLObject]) -> None: ...

    class tonConnectRegisterKey(TLObject):
        session_id: int
        client_id: str
        def __init__(self, *, session_id: int, client_id: str) -> None: ...

    class tonConnectSessions(TLObject):
        sessions: list[TLObject]
        def __init__(self, *, sessions: list[TLObject]) -> None: ...

    class tonConnectSubmitConnectResult(TLObject):
        error: bool
        session_id: int
        challenge_answer: bytes
        body: bytes
        trace_id: str | None
        def __init__(self, *, error: bool = ..., session_id: int, challenge_answer: bytes, body: bytes, trace_id: str | None = ...) -> None: ...

    class tonConnectSubmitResponse(TLObject):
        session_id: int
        msg_id: int
        body: bytes
        trace_id: str | None
        def __init__(self, *, session_id: int, msg_id: int, body: bytes, trace_id: str | None = ...) -> None: ...

    class transactions(TLObject):
        balance: int
        transactions: list[TLObject]
        next_offset: str | None
        chats: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, balance: int, transactions: list[TLObject], next_offset: str | None = ..., chats: list[TLObject], users: list[TLObject]) -> None: ...

    class userAddresses(TLObject):
        addresses: list[TLObject]
        users: list[TLObject]
        def __init__(self, *, addresses: list[TLObject], users: list[TLObject]) -> None: ...

class walletOwnershipProof(TLObject):
    timestamp: int
    signature: bytes
    def __init__(self, *, timestamp: int, signature: bytes) -> None: ...

class walletState(TLObject):
    backup_enabled: bool
    can_export_phrase: bool
    can_enable_backup: bool
    address: str
    public_key: bytes
    balance: int
    def __init__(self, *, backup_enabled: bool = ..., can_export_phrase: bool = ..., can_enable_backup: bool = ..., address: str, public_key: bytes, balance: int) -> None: ...

class walletStateEmpty(TLObject):
    creating: bool
    def __init__(self, *, creating: bool = ...) -> None: ...

class walletTransaction(TLObject):
    incoming: bool
    gasless: bool
    failed: bool
    key_change: bool
    comment_encrypted: bool
    id: str
    amount: int
    fee: int
    date: int
    peer: TLObject
    comment: str | None
    tx_hash: str | None
    nft: TLObject | None
    def __init__(self, *, incoming: bool = ..., gasless: bool = ..., failed: bool = ..., key_change: bool = ..., comment_encrypted: bool = ..., id: str, amount: int, fee: int, date: int, peer: TLObject, comment: str | None = ..., tx_hash: str | None = ..., nft: TLObject | None = ...) -> None: ...

class walletTransactionPeerAddress(TLObject):
    address: str
    domain: str | None
    def __init__(self, *, address: str, domain: str | None = ...) -> None: ...

class walletTransactionPeerChannel(TLObject):
    channel_id: int
    address: str
    domain: str | None
    def __init__(self, *, channel_id: int, address: str, domain: str | None = ...) -> None: ...

class walletTransactionPeerOnramp(TLObject):
    address: str
    domain: str | None
    provider_name: str
    def __init__(self, *, address: str, domain: str | None = ..., provider_name: str) -> None: ...

class walletTransactionPeerTelegramGift(TLObject):
    own_profile: bool
    def __init__(self, *, own_profile: bool = ...) -> None: ...

class walletTransactionPeerUnsupported(TLObject):
    def __init__(self) -> None: ...

class walletTransactionPeerUser(TLObject):
    user_id: int
    address: str
    domain: str | None
    def __init__(self, *, user_id: int, address: str, domain: str | None = ...) -> None: ...

class walletUserAddress(TLObject):
    user_id: int | None
    address: str
    public_key: bytes
    def __init__(self, *, user_id: int | None = ..., address: str, public_key: bytes) -> None: ...

class webAuthorization(TLObject):
    hash: int
    bot_id: int
    domain: str
    browser: str
    platform: str
    date_created: int
    date_active: int
    ip: str
    region: str
    def __init__(self, *, hash: int, bot_id: int, domain: str, browser: str, platform: str, date_created: int, date_active: int, ip: str, region: str) -> None: ...

class webDocument(TLObject):
    url: str
    access_hash: int
    size: int
    mime_type: str
    attributes: list[TLObject]
    def __init__(self, *, url: str, access_hash: int, size: int, mime_type: str, attributes: list[TLObject]) -> None: ...

class webDocumentNoProxy(TLObject):
    url: str
    size: int
    mime_type: str
    attributes: list[TLObject]
    def __init__(self, *, url: str, size: int, mime_type: str, attributes: list[TLObject]) -> None: ...

class webDomainException(TLObject):
    domain: str
    url: str
    title: str
    favicon: int | None
    def __init__(self, *, domain: str, url: str, title: str, favicon: int | None = ...) -> None: ...

class webPage(TLObject):
    has_large_media: bool
    video_cover_photo: bool
    id: int
    url: str
    display_url: str
    hash: int
    type: str | None
    site_name: str | None
    title: str | None
    description: str | None
    photo: TLObject | None
    embed_url: str | None
    embed_type: str | None
    embed_width: int | None
    embed_height: int | None
    duration: int | None
    author: str | None
    document: TLObject | None
    cached_page: TLObject | None
    attributes: list[TLObject] | None
    def __init__(self, *, has_large_media: bool = ..., video_cover_photo: bool = ..., id: int, url: str, display_url: str, hash: int, type: str | None = ..., site_name: str | None = ..., title: str | None = ..., description: str | None = ..., photo: TLObject | None = ..., embed_url: str | None = ..., embed_type: str | None = ..., embed_width: int | None = ..., embed_height: int | None = ..., duration: int | None = ..., author: str | None = ..., document: TLObject | None = ..., cached_page: TLObject | None = ..., attributes: list[TLObject] | None = ...) -> None: ...

class webPageAttributeAiComposeTone(TLObject):
    emoji_id: int
    def __init__(self, *, emoji_id: int) -> None: ...

class webPageAttributeStarGiftAuction(TLObject):
    gift: TLObject
    end_date: int
    def __init__(self, *, gift: TLObject, end_date: int) -> None: ...

class webPageAttributeStarGiftCollection(TLObject):
    icons: list[TLObject]
    def __init__(self, *, icons: list[TLObject]) -> None: ...

class webPageAttributeStickerSet(TLObject):
    emojis: bool
    text_color: bool
    stickers: list[TLObject]
    def __init__(self, *, emojis: bool = ..., text_color: bool = ..., stickers: list[TLObject]) -> None: ...

class webPageAttributeStory(TLObject):
    peer: TLObject
    id: int
    story: TLObject | None
    def __init__(self, *, peer: TLObject, id: int, story: TLObject | None = ...) -> None: ...

class webPageAttributeTheme(TLObject):
    documents: list[TLObject] | None
    settings: TLObject | None
    def __init__(self, *, documents: list[TLObject] | None = ..., settings: TLObject | None = ...) -> None: ...

class webPageAttributeUniqueStarGift(TLObject):
    gift: TLObject
    def __init__(self, *, gift: TLObject) -> None: ...

class webPageEmpty(TLObject):
    id: int
    url: str | None
    def __init__(self, *, id: int, url: str | None = ...) -> None: ...

class webPageNotModified(TLObject):
    cached_page_views: int | None
    def __init__(self, *, cached_page_views: int | None = ...) -> None: ...

class webPagePending(TLObject):
    id: int
    url: str | None
    date: int
    def __init__(self, *, id: int, url: str | None = ..., date: int) -> None: ...

class webViewMessageSent(TLObject):
    msg_id: TLObject | None
    def __init__(self, *, msg_id: TLObject | None = ...) -> None: ...

class webViewResultUrl(TLObject):
    fullsize: bool
    fullscreen: bool
    same_origin: bool
    query_id: int | None
    url: str
    def __init__(self, *, fullsize: bool = ..., fullscreen: bool = ..., same_origin: bool = ..., query_id: int | None = ..., url: str) -> None: ...

class widgetQueryTypeData(TLObject):
    with_wallet: bool
    def __init__(self, *, with_wallet: bool = ...) -> None: ...

class widgetQueryTypeSentTransaction(TLObject):
    wallet: TLObject
    msg_hash: str
    def __init__(self, *, wallet: TLObject, msg_hash: str) -> None: ...

class widgetQueryTypeSignData(TLObject):
    wallet: TLObject
    sign_data: TLObject
    def __init__(self, *, wallet: TLObject, sign_data: TLObject) -> None: ...
