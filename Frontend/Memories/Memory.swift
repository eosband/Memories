//
//  Memory.swift
//  Memories
//
//  Created by Chris Ward on 4/13/19.
//  Copyright © 2019 Chris Ward. All rights reserved.
//

import UIKit
import os.log

class Memory: NSObject, NSCoding {
    
    //MARK: Properties
    
    var title: String?
    var photo: UIImage?
    var text: String?
    var date: String?
    var id: String?
    
    //MARK: Archiving Points
    
    static let DocumentsDirectory = FileManager().urls(for: .documentDirectory, in: .userDomainMask).first!
    static let ArchiveURL = DocumentsDirectory.appendingPathComponent("memories")

    
    //MARK: Types
    
    struct PropertyKey{
        static let title = "title"
        static let photo = "photo"
        static let text = "text"
        static let date = "date"
        static let id = "id"
    }
    
    //MARK: Initializers
    init?(title: String, photo: UIImage?, text: String){
        // Name must not be empty
        guard !title.isEmpty else {
            return nil
        }
        
        // Initialize Stored Properties
        self.title = title
        self.photo = photo
        self.text = text
        
        // Initialize the Date
        // Formatting date as a String using DateFormatter from: https://stackoverflow.com/questions/39513258/get-current-date-in-swift-3/39514533
        
        let date = Date()
        let formatter = DateFormatter()
        formatter.dateFormat = "MM/dd/yyyy"
        self.date = formatter.string(from: date)
        
        // id will start as an empty string and will be set when memory is POSTed or from GET of all memories
        id = ""
    }
    
    //MARK: NSCoding
    func encode(with aCoder: NSCoder) {
        aCoder.encode(title, forKey: PropertyKey.title)
        aCoder.encode(photo, forKey: PropertyKey.photo)
        aCoder.encode(text, forKey: PropertyKey.text)
    }
    
    required convenience init?(coder aDecoder: NSCoder) {
        // The title is required. If we cannot decode a title string, the initializer should fail.
        guard let title = aDecoder.decodeObject(forKey: PropertyKey.title) as? String
            else {
                os_log("Unable to decode the title for a Memory object.", log: OSLog.default,
                       type: .debug)
                return nil
        }
        
        // Because photo is an optional property of Memory, just use conditional cast.
        let photo = aDecoder.decodeObject(forKey: PropertyKey.photo) as? UIImage
        
        // The text is required. If we cannot decode a text string, the initializer should fail.
        guard let text = aDecoder.decodeObject(forKey: PropertyKey.text) as? String
            else {
                os_log("Unable to decode the text for a Memory object.", log: OSLog.default,
                       type: .debug)
                return nil
        }
        
        // Must call designated initializer.
        self.init(title: title, photo: photo, text: text)
    }
}

