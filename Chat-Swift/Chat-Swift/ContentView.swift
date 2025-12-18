//
//  ContentView.swift
//  Chat-Swift
//
//  Created by Fatimah Alqarni on 18/12/2025.
//



import SwiftUI
import MessageUI

struct ContentView: View {

    @State private var showSMS = false
    @State private var showEmail = false

    let phoneNumber = "+966500000000"
    let emailAddress = "test@example.com"
    let randomMessage = "Hello from SwiftUI 👋"

    private let columns = [
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible())
    ]

    var body: some View {
        NavigationStack {
            HStack {
                VStack(spacing: 30) {

                    Text("Send Message")
                        .font(.title)
                        .padding(.top, 80.0)
                    
                    VStack(alignment: .leading, spacing: 20) {
                        HStack {
                            ShareButton(
                                title: "SMS",
                                icon: "message.fill",
                                color: .green
                            ) {
                                guard MFMessageComposeViewController.canSendText() else { return }
                                showSMS = true
                            }
                        }
                        
                        
                        HStack {
                            ShareButton(
                                title: "Email",
                                icon: "envelope.fill",
                                color: .orange
                            ) {
                                guard MFMailComposeViewController.canSendMail() else { return }
                                showEmail = true
                            }
                        }
                        
                        HStack {
                            ShareButton(
                                title: "AirDrop",
                                icon: "shareplay",
                                color: .blue
                            ) {
                                ShareService.shareAirDrop(message: randomMessage)
                            }
                        }
                    }
                    .padding(/*@START_MENU_TOKEN@*/.horizontal, 60.0/*@END_MENU_TOKEN@*/)

                    Spacer()
                }
                .navigationTitle("Simple Share")
                .sheet(isPresented: $showSMS) {
                    ShareService.SMSView(
                        phoneNumber: phoneNumber,
                        message: randomMessage
                    )
                }
                .sheet(isPresented: $showEmail) {
                    ShareService.MailView(
                        to: emailAddress,
                        subject: "Random Message",
                        body: randomMessage
                    )
                }
            }
        }
    }
}

struct ShareButton: View {

    let title: String
    let icon: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 10) {
                Image(systemName: icon)
                    .font(.system(size: 28, weight: .medium))
                Text(title)
                    .font(.subheadline.weight(.medium))
            }
            .foregroundColor(.white)
            .frame(maxWidth: .infinity, minHeight: 90)
            .background(color.gradient)
            .clipShape(RoundedRectangle(cornerRadius: 16))
        }
    }
}

// MARK: - ShareService
enum ShareService {

    // SMS / iMessage
    struct SMSView: UIViewControllerRepresentable {

        let phoneNumber: String
        let message: String

        func makeUIViewController(context: Context) -> MFMessageComposeViewController {
            let vc = MFMessageComposeViewController()
            vc.recipients = [phoneNumber]
            vc.body = message
            vc.messageComposeDelegate = context.coordinator
            return vc
        }

        func updateUIViewController(_ uiViewController: MFMessageComposeViewController, context: Context) {}
        func makeCoordinator() -> Coordinator { Coordinator() }

        class Coordinator: NSObject, MFMessageComposeViewControllerDelegate {
            func messageComposeViewController(_ controller: MFMessageComposeViewController,
                                              didFinishWith result: MessageComposeResult) {
                controller.dismiss(animated: true)
            }
        }
    }

    // Email
    struct MailView: UIViewControllerRepresentable {

        let to: String
        let subject: String
        let body: String

        func makeUIViewController(context: Context) -> MFMailComposeViewController {
            let vc = MFMailComposeViewController()
            vc.setToRecipients([to])
            vc.setSubject(subject)
            vc.setMessageBody(body, isHTML: false)
            vc.mailComposeDelegate = context.coordinator
            return vc
        }

        func updateUIViewController(_ uiViewController: MFMailComposeViewController, context: Context) {}
        func makeCoordinator() -> Coordinator { Coordinator() }

        class Coordinator: NSObject, MFMailComposeViewControllerDelegate {
            func mailComposeController(_ controller: MFMailComposeViewController,
                                       didFinishWith result: MFMailComposeResult,
                                       error: Error?) {
                controller.dismiss(animated: true)
            }
        }
    }

    // AirDrop
    static func shareAirDrop(message: String) {
        let activityVC = UIActivityViewController(activityItems: [message], applicationActivities: nil)

        if let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
           let root = scene.windows.first?.rootViewController {
            root.present(activityVC, animated: true)
        }
    }
}

#Preview {
    ContentView()
}

