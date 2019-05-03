//
//  MemoryTableViewCell.swift
//  Memories
//
//  Created by Chris Ward on 4/14/19.
//  Copyright © 2019 Chris Ward. All rights reserved.
//

import UIKit

class MemoryTableViewCell: UITableViewCell {
    //MARK: Properties
    
    @IBOutlet weak var title: UILabel!
    @IBOutlet weak var photoImageView: UIImageView!
    @IBOutlet weak var date: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
